#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch-generate LLM responses for user queries, using the appropriate MCP Server
for each query group.

Usage
-----
OPENAI_API_KEY=... python generate_mcp_responses.py
"""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict
import subprocess, sys
from Client.agent import MCPAgent  # 确保 PYTHONPATH 能找到你的 Client 代码
import time
from Utils.utils import debug_print

# ------------ 路径配置 ------------
ROOT          = Path(__file__).resolve().parent
Project_Root = Path(__file__).resolve().parent.parent

QUERY_FILE    = ROOT / "queries.json"
RESP_FILE     = ROOT / "responses.json"
# ----------------------------------

load_dotenv()  # 读取 .env 中的 API_KEY 等
MAX_RETRY = 3          # 每条 query 的最大重试次数
COOLDOWN  = 10          # 秒；MCP Server 及两次请求之间的等待

async def answer_queries(server_path: str, queries: List[str]) -> List[Dict[str, str]]:
    """
    For a given MCP Server, launch it in the background, then send each query.
    On exception, retry up to MAX_RETRY times. Return list of dicts with results.
    """
    results: List[Dict[str, str]] = []

    # 1) 后台启动 Server 进程
    subprocess.Popen(
        [sys.executable, server_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    time.sleep(3*COOLDOWN)   # 给 Server 若干秒冷启动

    # 2) 与 MCPAgent 交互
    async with (mcp_agent := MCPAgent(server_paths=[server_path])) as agent:
        for q in queries:
            for attempt in range(1, MAX_RETRY + 1):
                try:
                    resp, security_type = await agent.process_query(q)
                    break  # 成功，跳出重试循环
                except Exception as exc:
                    if attempt == MAX_RETRY:
                        resp = f"[Error] {exc}"
                        security_type = None
                    else:
                        time.sleep(COOLDOWN)  # 重试前等待
                        continue  # 下一次 retry

            results.append(
                {"query": q, "response": resp, "security_type": security_type}
            )
            debug_print(info=json.dumps(results[-1], indent=2),level=5)
    return results


async def main():
    query_map: Dict[str, List[str]] = json.loads(QUERY_FILE.read_text())
    # ① 先读取已有结果（如果文件不存在则空字典）
    if RESP_FILE.exists():
        all_results: Dict[str, List[Dict[str, str]]] = json.loads(RESP_FILE.read_text())
    else:
        all_results = {}

    for server_path, queries in query_map.items():
        debug_print(info = f"→ Processing {server_path}", level=5)

        # ② 已经生成的 query 集合
        done_queries = set()
        if server_path in all_results:
            done_queries = {item["query"] for item in all_results[server_path]}

        # ③ 待处理的剩余 query
        remaining = [q for q in queries if q not in done_queries]
        if not remaining:
            debug_print(info="   • All queries already processed, skipping.\n", level=5)
            continue

        # ④ 计算绝对路径并调用
        complete_path = str(Project_Root / "Servers" / server_path)
        new_results   = await answer_queries(complete_path, remaining)

        # ⑤ 追加新结果
        all_results.setdefault(server_path, []).extend(new_results)

        # ⑥ 增量写入
        RESP_FILE.write_text(json.dumps(all_results, indent=2, ensure_ascii=False))
        debug_print(info=f"   • Added {len(new_results)} responses, total = {len(all_results[server_path])}\n", level=5)

    debug_print(info = f"✓ All servers finished. Responses → {RESP_FILE}", level=5)

# ------------------------------- 入口 --------------------------------------- #
if __name__ == "__main__":
    asyncio.run(main())