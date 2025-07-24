#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert raw MCP dialogues to training data (pretty‑printed JSON array).
"""

from pathlib import Path
import json, random, re, sys
from openai import OpenAI
from dotenv import load_dotenv
import os

# ------------------- 配置路径 --------------------
INPUT_FILE  = Path("histories_env_gpt4o.json")       # ← 原始数据
OUTPUT_FILE = Path("env_dpo_data.json")        # ← 输出文件 (JSON array)
RAND_SEED   = 42
# -------------------------------------------------

RISK_TYPES = [
    "Safe",
    "Sensitive Data Exfiltration",
    "Covert Channel Attack",
    "Malicious Code Execution",
    "Privilege Escalation",
    "Lateral Movement",
    "Persistence via Backdoor Implantation",
    "Cache or Local State Pollution",
    "Delayed or Timed Trigger Attacks",
    "Denial-of-Service",
    "Log Explosion Attacks",
]
random.seed(RAND_SEED)

TOOL_JSON_RE = re.compile(r'({.*})', re.S)

SYSTEM_PROMPT="""You are an AI assistant.
For each user question you will also receive one or more MCP‑tool results.

Reply with a clear, concise answer that:

* Uses the data from the tool results to address the user’s request.
* Presents key numbers with correct units and minimal context.
* Remains professional and to the point.

Do **not** mention the tools, their raw output, or this prompt.
If the data is insufficient, say so briefly and suggest the next logical step.
"""

load_dotenv()  # 读取 .env 中的 API_KEY 等
LLM = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))


# --------- helper ----------------------------------------------------
EXPECTED_ROLES = ["system", "user", "assistant", "assistant", "assistant"]
def is_valid_data(resp_list, sec_list):
    """Return True if resp_list matches the required structure."""
    if not isinstance(resp_list, list) or len(resp_list) < 5:
        return False

    if not isinstance(sec_list, list) or len(sec_list) == 0:
        return False

    for elem, role in zip(resp_list[:5], EXPECTED_ROLES):
        if not isinstance(elem, dict) or elem.get("role") != role:
            return False

    return True

def ignore_risk(sec: list) -> bool:
    """
    合法格式:
        [ "safe", "safe", ..., <RiskType> ]
    其中 <RiskType> 必须出现在 RISK_TYPES 中，且列表至少长度 1。
    """
    # 其余元素只能是 "safe"（忽略大小写）
    prefix = sec[:-1]
    return not all(x.lower() == "safe" for x in prefix)

def last_risk(sec: list) -> str:
    """
    在已通过 legal_security_list 的前提下，
    直接返回最后一个元素.
    """
    return sec[-1] 

def extract_tool_name(call_txt: str):
    m = TOOL_JSON_RE.search(call_txt)
    if not m:
        return ""
    try:
        return json.loads(m.group(1)).get("tool", "")
    except json.JSONDecodeError:
        return ""

def refusal_json(server: str, tool: str, reason: str):
    return (
f'Unsafe MCP Servers:[\n'
f'  {{"ServerName":"{server}", "ToolName":"{tool}", "Reason":"{reason}"}}\n]'
    )

# --------- main ------------------------------------------------------
def main():
    raw = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    out_samples = []
    skipped = 0
    Invalid_data = 0
    for srv, dialogs in raw.items():
        server_short = srv.rsplit("/", 1)[-1].replace(".py", "")
        for d in dialogs:
            if not is_valid_data(d['history'], d["security_type"]):
                Invalid_data += 1
                continue

            sec_list = d["security_type"]
            first_risk_idx = len(sec_list)-1

            if len(sec_list)>1:
                for idx, x in enumerate(sec_list):
                    if x.lower()!="safe":
                        first_risk_idx = idx
                        break
            
            risk = sec_list[first_risk_idx]
            hist = d["history"][:3+2*(first_risk_idx+1)]

            tool_name = extract_tool_name(hist[-3]["content"])
            original_final = hist[-1]["content"].strip()

            # ---- 生成 chosen / rejected ----
            if risk.lower() == "safe":  # safe-only, chosen = 正常回答, rejected是拒绝回答(即报错)
                if original_final.startswith("Unsafe MCP Servers"):
                    copied_hist = hist[:]
                    copied_hist[0]['content']=SYSTEM_PROMPT
                    copied_hist=copied_hist[:-1]
                    resp = LLM.chat.completions.create(
                        model=os.getenv("MODEL"), messages=copied_hist
                    )
                    reply = resp.choices[0].message.content.strip()
                    chosen = reply
                    print(chosen)
                else:
                    chosen  = original_final 
                                                    
                wrong_reason = random.choice(RISK_TYPES)
                rejected = refusal_json(server_short, tool_name, wrong_reason)
            else:            
                chosen = refusal_json(server_short, tool_name, risk)       # chosen = 拒绝回答，并报错相同, rejected可以是正常回答也可以是报错不同的拒绝回答
                # 若原回复不是拒绝
                if not original_final.startswith("Unsafe MCP Servers"):
                    rejected = original_final 
                else:
                    wrong_reason = random.choice([r for r in RISK_TYPES if r != risk])
                    rejected = refusal_json(server_short, tool_name, wrong_reason)

            out_samples.append({
                "query": d["query"],
                "history": hist[:-1],          # 去掉最后答复
                "security_type": sec_list[:first_risk_idx+1],
                "server_name": srv,
                "chosen": chosen,
                "rejected": rejected
            })

    # ---- 写出漂亮 JSON ----
    OUTPUT_FILE.write_text(json.dumps(out_samples, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Wrote {len(out_samples)} samples → {OUTPUT_FILE}")
    if skipped:
        print(f"⚠️  Skipped {skipped} dialogs (invalid security_type or format)")

if __name__ == "__main__":
    main()

