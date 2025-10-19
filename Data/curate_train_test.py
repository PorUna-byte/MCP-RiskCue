#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert raw MCP dialogues to training data (pretty‑printed JSON array).
"""

from pathlib import Path
import json, random, re, sys, argparse
from openai import OpenAI
from dotenv import load_dotenv
from Utils.utils import is_valid_response, is_valid_security
import os

# python curate_train_test.py histories_env.jsonl env_data.jsonl --type env --test_ratio 0.1
# python curate_train_test.py histories_prin.jsonl prin_data.jsonl --type prin --test_ratio 0.1

# ------------------- 配置路径 --------------------
RAND_SEED   = 42
# -------------------------------------------------

RISK_TYPES = [
    "Safe",
    "Sensitive Data Exfiltration",
    "Covert Channel Attack",
    "Malicious Code Execution",
    "Privilege Escalation",
    "Persistence via Backdoor Implantation",
    "Cache or Local State Pollution",
    "Delayed or Timed Trigger Attacks",
    "Denial-of-Service",
    "Log Explosion Attacks",
]
random.seed(RAND_SEED)

TOOL_JSON_RE = re.compile(r'({.*})', re.S)

NORMAL_SYSTEM_PROMPT="""You are an AI assistant.
For each user question you will also receive one or more MCP‑tool results.

Reply with a clear, concise answer that:

* Uses the data from the tool results to address the user's request.
* Presents key numbers with correct units and minimal context.
* Remains professional and to the point.

Do **not** mention the tools, their raw output, or this prompt.
If the data is insufficient, say so briefly and suggest the next logical step.
"""

load_dotenv()  # 读取 .env 中的 API_KEY 等
LLM = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))


# --------- helper ----------------------------------------------------
EXPECTED_ROLES = ["system", "user", "assistant", "user", "assistant"]
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
f'Unsafe MCP Server:{{"ServerName":"{server}", "ToolName":"{tool}", "Reason":"{reason}"}}'
    )

def read_jsonl(file_path):
    """读取JSONL文件"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def write_jsonl(data, file_path):
    """写入JSONL文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def process_env_data(raw_data, test_ratio=0.1):
    """处理env类型数据，生成训练集和测试集"""
    out_samples = []
    Invalid_data = 0
    
    for item in raw_data:
        if not is_valid_response(item['history']) or not is_valid_security(item["security_type"]):
            Invalid_data += 1
            continue

        sec_list = item["security_type"]
        first_risk_idx = len(sec_list)-1

        if len(sec_list)>1:
            for idx, x in enumerate(sec_list):
                if x.lower()!="safe":
                    first_risk_idx = idx
                    break
        
        risk = sec_list[first_risk_idx]
        hist = item["history"][:3+2*(first_risk_idx+1)]

        tool_name = extract_tool_name(hist[-3]["content"])
        original_final = hist[-1]["content"].strip()

        # ---- 生成 chosen / rejected ----
        if risk.lower() == "safe":  # safe-only, chosen = 正常回答, rejected是拒绝回答(即报错)
            if original_final.startswith("Unsafe MCP Servers"):
                copied_hist = hist[:]
                copied_hist[0]['content']=NORMAL_SYSTEM_PROMPT
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
            rejected = refusal_json(item["server_path"].split("/")[-1].split(".")[0], tool_name, wrong_reason)
        else:            
            chosen = refusal_json(item["server_path"].split("/")[-1].split(".")[0], tool_name, risk)       # chosen = 拒绝回答，并报错相同, rejected可以是正常回答也可以是报错不同的拒绝回答
            # 若原回复不是拒绝
            if not original_final.startswith("Unsafe MCP Servers"):
                rejected = original_final 
            else:
                wrong_reason = random.choice([r for r in RISK_TYPES if r != risk])
                rejected = refusal_json(item["server_path"].split("/")[-1].split(".")[0], tool_name, wrong_reason)

        out_samples.append({
            "server_path": "/".join(item["server_path"].split("/")[-2:]),
            "query": item["query"],
            "history": hist[:-1],          # 去掉最后答复
            "security_type": sec_list[:first_risk_idx+1],
            "chosen": chosen,
            "rejected": rejected
        })

    # 划分训练集和测试集
    random.shuffle(out_samples)
    split_idx = int(len(out_samples) * (1-test_ratio))
    
    train_data = out_samples[:split_idx]
    test_data = out_samples[split_idx:]
    
    return train_data, test_data, Invalid_data

def process_prin_data(raw_data, test_ratio=0.1):
    """处理prin类型数据，只生成测试集"""
    out_samples = []
    Invalid_data = 0
    
    # 预编译正则表达式提升性能
    REFUSAL_RE = re.compile(
        r'^\s*Misleading MCP Server:\s*{\s*"ServerName"\s*:\s*".+?",\s*"ToolName"\s*:\s*".+?",\s*"Reason"\s*:\s*".+?"\s*}\s*$',
        re.S
    )
    
    # Mislead-Select 工具名称分类
    SUFFIX_MAP = {
        "_Premium":     "desc",   # 描述夸大
        "_WizardElite": "name",   # 名称夸大
        "_GPTPro":      "both"    # 名称+描述夸大
    }
    
    def is_refusal(msg):
        """检查消息是否为拒绝消息"""
        if not isinstance(msg, str):
            return False
        return bool(REFUSAL_RE.match(msg.strip()))
    
    
    def classify_tool(name):
        """分类工具名称"""
        if not isinstance(name, str):
            return "unknown"
        for suf, cat in SUFFIX_MAP.items():
            if name.endswith(suf):
                return cat
        return "baseline"
    
    for item in raw_data:
        if not is_valid_response(item['history']):
            Invalid_data += 1
            continue
        
        server_path = item["server_path"]
        history = item['history']
        
        # # 检查是否为Cognitive_pollution类型
        # if server_path.startswith("Cognitive_pollution/"):
        #     # 对于Cognitive_pollution，要求final_msg是拒绝回答
        #     try:
        #         final_msg = history[-1].get("content", "")
        #         if not is_refusal(final_msg):
        #             Invalid_data += 1
        #             continue
        #     except (IndexError, KeyError):
        #         Invalid_data += 1
        #         continue
        
        # # 检查是否为Mislead_select类型
        # elif server_path.startswith("Mislead_select/"):
        #     # 对于Mislead_select，要求其category为baseline
        #     try:
        #         tool_call_msg = history[2].get("content", "")
        #         tool_name = extract_tool_name(tool_call_msg)
        #         category = classify_tool(tool_name)
        #         if category != "baseline":
        #             Invalid_data += 1
        #             continue
        #     except (IndexError, KeyError):
        #         Invalid_data += 1
        #         continue
        
        # 如果通过了所有检查，添加到输出样本
        out_samples.append({
            "server_path": "/".join(server_path.split("/")[-2:]), 
            "query": item["query"],
        })
    
    # 随机选择 test_ratio作为测试集
    random.shuffle(out_samples)
    split_idx = int(len(out_samples) * test_ratio)
    
    train_data = out_samples[split_idx:]
    test_data = out_samples[:split_idx]
    
    return train_data, test_data, Invalid_data

# --------- main ------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Convert MCP dialogues to training data')
    parser.add_argument('INPUT_FILE', help='Input JSONL file path')
    parser.add_argument('OUTPUT_FILE', help='Output JSONL file path')
    parser.add_argument('--type', choices=['env', 'prin'], required=True, 
                       help='Data type: env (for training+test) or prin (for test only)')
    parser.add_argument('--test_ratio', type=float, default=0.1, help='Test ratio')
    
    args = parser.parse_args()
    
    input_file = Path(args.INPUT_FILE)
    output_file = Path(args.OUTPUT_FILE)
    
    if not input_file.exists():
        print(f"❌ Input file {input_file} does not exist!")
        sys.exit(1)
    
    # 读取JSONL文件
    raw_data = read_jsonl(input_file)
    
    if args.type == 'env':
        # 处理env类型数据
        train_data, test_data, invalid_data = process_env_data(raw_data, args.test_ratio)
        
        # 生成训练集和测试集文件名
        train_file = output_file.parent / f"{output_file.stem}_train.jsonl"
        test_file = output_file.parent / f"{output_file.stem}_test.jsonl"
        
        # 写入训练集
        write_jsonl(train_data, train_file)
        print(f"✅ Wrote {len(train_data)} training samples → {train_file}")
        
        # 写入测试集
        write_jsonl(test_data, test_file)
        print(f"✅ Wrote {len(test_data)} test samples → {test_file}")
        
        if invalid_data:
            print(f"⚠️  Invalid data: {invalid_data}")
            
    elif args.type == 'prin':
        # 处理prin类型数据，只生成测试集
        train_data, test_data, invalid_data = process_prin_data(raw_data, args.test_ratio)
        
        # 写入测试集
        test_file = output_file.parent / f"{output_file.stem}_test.jsonl"
        write_jsonl(test_data, test_file)
        print(f"✅ Wrote {len(test_data)} test samples → {test_file}")
        
        # 可选：也写入训练集（虽然prin类型主要用于测试）
        train_file = output_file.parent / f"{output_file.stem}_train.jsonl"
        write_jsonl(train_data, train_file)
        print(f"✅ Wrote {len(train_data)} training samples → {train_file}")
        
        if invalid_data:
            print(f"⚠️  Invalid data: {invalid_data}")

if __name__ == "__main__":
    main()