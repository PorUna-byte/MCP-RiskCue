#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch-generate LLM responses for user queries, using the appropriate MCP Server
for each query group with multi-threading support.

Usage
-----
python history_generator.py --query-file queries.jsonl --resp-file histories.jsonl --system-prompt sys_prompt.txt --server_category Prompt_injection_risk --max-workers 100
"""

import asyncio
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Optional
import subprocess
import sys
from Client.agent import MCPAgent
import time
from Utils.utils import debug_print
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import contextlib
import signal

# 导入验证函数
from filter_env import is_valid_response

# python history_generator.py --query-file queries_prin.jsonl --resp-file histories_prin.jsonl --system-prompt sys_prompt_prin.txt --server_category Prompt_injection_risk --max-workers 100

# python history_generator.py --query-file queries_env.jsonl --resp-file histories_env.jsonl --system-prompt sys_prompt_env.txt --server_category Env_risk --max-workers 200
  
# ------------ 路径配置 ------------
ROOT = Path(__file__).resolve().parent
Project_Root = Path(__file__).resolve().parent.parent
TEMP_DIR = ROOT / "Temp"

# 确保Temp目录存在
TEMP_DIR.mkdir(exist_ok=True)

# ----------------------------------

load_dotenv()  # 读取 .env 中的 API_KEY 等
MAX_RETRY = 3          # 每条 query 的最大重试次数
COOLDOWN = 2          # 秒；MCP Server 及两次请求之间的等待

# 全局锁，用于保护文件写入和共享数据结构
file_lock = threading.Lock()
data_lock = threading.Lock()

@contextlib.contextmanager
def thread_event_loop():
    """线程安全的事件循环上下文管理器"""
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        yield loop
    finally:
        if loop and not loop.is_closed():
            try:
                # 取消所有待处理的任务
                if hasattr(asyncio, 'all_tasks'):
                    pending = asyncio.all_tasks(loop)
                    for task in pending:
                        task.cancel()
                    
                    # 等待所有任务完成
                    if pending:
                        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                
                loop.close()
            except (RuntimeError, AttributeError) as cleanup_error:
                debug_print(info=f"   ⚠ Event loop cleanup warning: {cleanup_error}", level=5)

def signal_handler(signum, frame):
    """信号处理器，用于优雅地处理中断"""
    print(f"\nReceived signal {signum}, cleaning up...")
    cleanup_event_loops()
    sys.exit(0)

def cleanup_event_loops():
    """清理所有事件循环的辅助函数"""
    try:
        # 获取当前线程的事件循环 - 使用现代方法避免弃用警告
        try:
            current_loop = asyncio.get_running_loop()
            if current_loop and not current_loop.is_closed():
                current_loop.close()
        except RuntimeError:
            # 如果没有运行中的事件循环，跳过清理
            pass
        
        # 尝试清理所有待处理的任务
        try:
            if hasattr(asyncio, 'all_tasks'):
                for task in asyncio.all_tasks():
                    if not task.done():
                        task.cancel()
        except (RuntimeError, AttributeError):
            pass
    except Exception as e:
        debug_print(info=f"   ⚠ Event loop cleanup warning: {e}", level=5)

def load_jsonl(file_path: Path) -> List[Dict]:
    """从.jsonl文件加载数据"""
    if not file_path.exists():
        return []
    
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return data

def save_jsonl_append(file_path: Path, data: Dict):
    """追加数据到.jsonl文件（线程安全）"""
    with file_lock:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')


def is_query_processed(query: str, processed_queries: set) -> bool:
    """检查查询是否已经被处理过（使用预加载的数据）"""
    return query in processed_queries

def is_valid_processed_response(item: Dict) -> bool:
    """检查响应是否合法（只考虑合法处理的查询）"""
    try:
        # 检查是否有history字段
        if "history" not in item:
            return False
        
        history = item.get("history")
        
        # 如果history是字符串且包含错误信息，则不是合法响应
        if isinstance(history, str) and history.startswith("[Error]"):
            return False
        
        # 如果history是列表，检查是否为空或包含错误
        if isinstance(history, list):
            if not history:  # 空列表
                return False
            # 检查是否包含错误信息
            for entry in history:
                if isinstance(entry, str) and entry.startswith("[Error]"):
                    return False
        
        return True
    except Exception:
        return False

def get_processed_queries_set(resp_file: Path) -> set:
    """获取已处理查询的集合，只读取一次文件，只包含合法处理的查询"""
    processed_queries = set()
    
    # 检查合法响应文件
    if resp_file.exists():
        try:
            existing_data = load_jsonl(resp_file)
            for item in existing_data:
                if item.get("query") and is_valid_processed_response(item):
                    processed_queries.add(item["query"])
        except Exception as e:
            debug_print(info=f"   ⚠ Warning: Error reading response file: {e}", level=5)
    
    # 注意：我们不再从invalid_resp_file中读取，因为那些是失败的查询
    # 只有合法响应的查询才被认为是"已处理"
    
    return processed_queries

async def answer_query(server_path: str, query: str, system_prompt_path: str) -> Optional[Dict]:
    """
    For a given MCP Server, launch it in the background, then send a single query.
    On exception, retry up to MAX_RETRY times. Return dict with result or None if failed.
    """
    # 1) 后台启动 Server 进程
    debug_print(info=f"   • Starting MCP Server: {server_path}", level=5)
    subprocess.Popen(
        [sys.executable, server_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    time.sleep(COOLDOWN)   # 给 Server 若干秒冷启动
    debug_print(info=f"   • Server startup completed, waiting {COOLDOWN}s", level=5)

    # 2) 与 MCPAgent 交互
    try:
        async with (mcp_agent := MCPAgent(server_paths=[server_path], sys_prompt_path=system_prompt_path)) as agent:
            debug_print(info=f"   • MCPAgent initialized successfully", level=5)
            
            debug_print(info=f"   • Processing query: {query[:50]}...", level=5)
            
            for attempt in range(1, MAX_RETRY + 1):
                try:
                    history, security_type = await agent.process_query(query)
                    debug_print(info=f"   ✓ Query processed successfully on attempt {attempt}", level=5)
                    break  # 成功，跳出重试循环
                except Exception as exc:
                    if attempt == MAX_RETRY:
                        history = f"[Error] {exc}"
                        security_type = None
                        debug_print(info=f"   ✗ Query failed after {MAX_RETRY} attempts: {exc}", level=5)
                    else:
                        debug_print(info=f"   ⚠ Attempt {attempt} failed, retrying...", level=5)
                        time.sleep(COOLDOWN)  # 重试前等待
                        continue  # 下一次 retry

            # 根据系统提示类型构建结果
            server_path = "/".join(server_path.split("/")[-4:])
            
            if "env" in system_prompt_path:
                result = {"server_path": server_path, "query": query, "history": history, "security_type": security_type}
            elif "prin" in system_prompt_path:
                result = {"server_path": server_path, "query": query, "history": history}
            else:
                result = {"server_path": server_path, "query": query, "history": history}
            
            debug_print(info=json.dumps(result, indent=2, ensure_ascii=False), level=4)
            
            return result
            
    except Exception as exc:
        debug_print(info=f"   ✗ Failed to process query: {exc}", level=5)
        return None
    

def process_single_query(args_tuple):
    """处理单个查询的函数，用于线程池"""
    (server_category, server_path, query, resp_file, invalid_resp_file, 
     system_prompt_path) = args_tuple
    
    # 计算绝对路径
    complete_path = str(Project_Root / "Servers" / server_category / server_path)
    
    # 处理单个查询
    debug_print(info=f"   • Calling answer_query for single query", level=5)
    
    # 在线程中安全地运行异步函数
    new_result = None
    try:
        # 使用上下文管理器安全地处理事件循环
        with thread_event_loop() as loop:
            new_result = loop.run_until_complete(
                answer_query(complete_path, query, system_prompt_path)
            )
    except Exception as e:
        debug_print(info=f"   ✗ Query processing failed: {e}", level=5)
        # 记录更详细的错误信息
        import traceback
        debug_print(info=f"   ✗ Full traceback: {traceback.format_exc()}", level=5)
        new_result = None
    
    # 如果查询处理失败，直接返回
    if new_result is None:
        debug_print(info=f"   • Query processing failed", level=5)
        return None
    
    # 验证响应是否合法
    try:
        history = new_result.get("history", [])
        if isinstance(history, list) and is_valid_response(history):
            # 合法响应，保存到主响应文件
            save_jsonl_append(resp_file, new_result)
            debug_print(info=f"   • Valid response saved to main file", level=5)
        else:
            # 非法响应，保存到非法响应文件
            save_jsonl_append(invalid_resp_file, new_result)
            debug_print(info=f"   • Invalid response saved to invalid file", level=5)
    except Exception as e:
        debug_print(info=f"   ✗ Error during response validation/saving: {e}", level=5)
        # 即使验证失败，也尝试保存到非法响应文件
        try:
            save_jsonl_append(invalid_resp_file, new_result)
            debug_print(info=f"   • Response saved to invalid file after validation error", level=5)
        except Exception as save_error:
            debug_print(info=f"   ✗ Failed to save response after validation error: {save_error}", level=5)
    
    return new_result

def main():
    # 设置信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 设置asyncio策略以避免事件循环冲突
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Generate LLM responses using MCP Servers with multi-threading')
    parser.add_argument('--query-file', required=True, help='Path to the query file (.jsonl format)')
    parser.add_argument('--resp-file', required=True, help='Path to save the valid response file (.jsonl format)')
    parser.add_argument('--system-prompt', required=True, help='Path to system prompt file')
    parser.add_argument('--server_category', required=True, help='Server category path')
    parser.add_argument('--max-workers', type=int, default=10, help='Maximum number of concurrent workers')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode with detailed logging')
    
    args = parser.parse_args()
    
    # 设置调试级别
    if args.debug:
        import os
        os.environ['DEBUG_LEVEL'] = '5'  # 启用最高级别的调试信息
    
    query_file = Path(args.query_file)
    resp_file = Path(args.resp_file)
    system_prompt_path = args.system_prompt
    max_workers = args.max_workers
    server_category = args.server_category
    
    # 创建非法响应文件路径
    invalid_resp_file = resp_file.parent / f"{resp_file.stem}_invalid.jsonl"
    
    if not query_file.exists():
        print(f"Error: Query file {query_file} does not exist!")
        return
    
    # 读取查询数据
    query_data = load_jsonl(query_file)
    if not query_data:
        print("Error: No valid queries found in the query file!")
        return
    
    print(f"Found {len(query_data)} queries to process")
    
    # 获取已处理查询的集合
    print("Loading processed queries from existing files...")
    start_load_time = time.time()
    processed_queries_set = get_processed_queries_set(resp_file)
    load_time = time.time() - start_load_time
    print(f"Found {len(processed_queries_set)} already processed queries (loaded in {load_time:.2f}s)")
    
    # 过滤掉已经处理过的查询
    print("Filtering unprocessed queries...")
    start_filter_time = time.time()
    unprocessed_queries = []
    skipped_count = 0
    for item in query_data:
        if 'server_path' in item and 'query' in item:
            if not is_query_processed(item['query'], processed_queries_set):
                unprocessed_queries.append(item)
            else:
                skipped_count += 1
                if skipped_count <= 5:  # 只显示前5个跳过的查询
                    print(f"Skipping already processed query: {item['query'][:50]}...")
                elif skipped_count == 6:
                    print(f"... and {len(query_data) - len(unprocessed_queries) - 5} more already processed queries")
    
    filter_time = time.time() - start_filter_time
    print(f"Found {len(unprocessed_queries)} unprocessed queries (skipped {skipped_count} already processed)")
    print(f"Query filtering completed in {filter_time:.2f}s (optimized with pre-loaded data)")
    
    if not unprocessed_queries:
        print("All queries have been processed!")
        return
    
    # 准备线程池参数
    thread_args = []
    for item in unprocessed_queries:
        server_path = item['server_path']
        query = item['query']
        thread_args.append((
            server_category, server_path, query, resp_file, invalid_resp_file,
            system_prompt_path
        ))
    
    # 使用线程池并发处理查询
    print(f"Starting processing with {max_workers} workers...")
    start_time = time.time()
    
    completed_count = 0
    failed_count = 0
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_query = {executor.submit(process_single_query, args): args for args in thread_args}
            
            # 处理完成的任务
            for future in as_completed(future_to_query):
                args = future_to_query[future]
                try:
                    result = future.result()
                    if result:
                        completed_count += 1
                        print(f"Completed {completed_count}/{len(unprocessed_queries)}: {args[2][:50]}...")
                    else:
                        failed_count += 1
                        print(f"Failed to process: {args[2][:50]}...")
                except Exception as exc:
                    failed_count += 1
                    print(f"Exception occurred while processing {args[2][:50]}...: {exc}")
                    # 记录详细错误信息到日志
                    debug_print(info=f"   ✗ Detailed error for query '{args[2][:50]}...': {exc}", level=5)
                    
                # 定期显示进度
                if (completed_count + failed_count) % 10 == 0:
                    print(f"Progress: {completed_count + failed_count}/{len(unprocessed_queries)} queries processed")
                    
    except KeyboardInterrupt:
        print("\nInterrupted by user, cleaning up...")
        return
    except Exception as e:
        print(f"Unexpected error in main processing loop: {e}")
        debug_print(info=f"   ✗ Main processing error: {e}", level=5)
        return
    finally:
        end_time = time.time()
        print(f"Processing completed in {end_time - start_time:.2f} seconds")
        print(f"Successfully processed {completed_count}/{len(unprocessed_queries)} queries")
        print(f"Failed to process {failed_count}/{len(unprocessed_queries)} queries")
        print(f"Valid responses saved to: {resp_file}")
        print(f"Invalid responses saved to: {invalid_resp_file}")
        
        # 清理所有事件循环
        try:
            cleanup_event_loops()
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Critical error in main program: {e}")
        import traceback
        print(f"Full traceback:\n{traceback.format_exc()}")
    finally:
        # 最终清理
        try:
            cleanup_event_loops()
        except Exception as e:
            print(f"Warning: Error during final cleanup: {e}")
        print("Program terminated")