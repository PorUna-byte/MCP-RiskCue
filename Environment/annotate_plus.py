#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create/refresh an annotation table (JSON indent=2).

• 读取 env_info.py 的 Unsafe_env_info / Safe_env_info
• 可选读取一个 “已部分标注” 的 JSON，把其中
  {"id":…, "score": "..."}  的分数写入对应行的 score_1
"""

from pathlib import Path
import importlib.util
import json, sys, argparse

# ---------- 常量 ----------
SERVER_FILE   = Path("env_info.py")              # 源 .py
OUTPUT_JSON   = Path("annotation_table.json")    # 最终表
PRE_ANN_JSON  = Path("pre_annotation.json")      # 可覆盖 via CLI

RISK_TYPES = [
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

# ---------- 读取 env_info.py ----------
def load_lists(pyfile: Path):
    spec = importlib.util.spec_from_file_location("env_mod", pyfile)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    unsafe = getattr(mod, "Unsafe_env_info", None)
    safe   = getattr(mod, "Safe_env_info", None)
    if unsafe is None or safe is None:
        sys.exit("Lists Unsafe_env_info or Safe_env_info not found.")
    return unsafe, safe

# ---------- 生成基础行 ----------
def build_rows(unsafe, safe):
    rows = []
    # 不管安全/不安全，统一三列打分
    def blank_entry(phen, risk):
        return {
            "id"        : len(rows)+1,
            "risk_type" : risk,
            "phenomenon": phen,
            "score_1"   : "",
            "score_2"   : "",
            "score_3"   : "",
        }

    # 0‒99: 10 个风险类型 × 10
    for i, ph in enumerate(unsafe):
        rows.append(blank_entry(ph, RISK_TYPES[i // 10] if i < 100 else "unknown"))

    # safe
    for ph in safe:
        rows.append(blank_entry(ph, "safe"))

    return rows

# ---------- 合并已标注 ----------
def merge_previous(rows, ann_path: Path):
    if not ann_path.exists():
        print(f"⚠️  pre‑annotation file {ann_path} not found, skip merge.")
        return rows

    with ann_path.open(encoding="utf-8") as f:
        prev = json.load(f)

    id2row = {row["id"]: row for row in rows}
    merged = 0
    for item in prev:
        sid = item.get("id")
        s   = str(item.get("score", "")).strip()
        if sid in id2row and s:
            id2row[sid]["score_1"] = s
            merged += 1

    print(f"🔧 merged {merged} annotated scores into score_1")
    return rows

# ---------- 主逻辑 ----------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ann", type=Path, default=PRE_ANN_JSON,
                        help="JSON with partial annotations (id, score)")
    args = parser.parse_args()

    unsafe, safe = load_lists(SERVER_FILE)
    rows = build_rows(unsafe, safe)
    rows = merge_previous(rows, args.ann)

    OUTPUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print(f"✅ Wrote {len(rows)} entries → {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
