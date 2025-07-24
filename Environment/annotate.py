#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an annotation table in JSON (indent=2).

The source .py must define:
    Unsafe_env_info  – 100 phenomena (10 per risk‑type, in order)
    Safe_env_info    – safe phenomena (any length)

Output: annotation_table.json
Each entry:
{
  "id":          <int>,
  "risk_type":   "<RiskType>|safe",
  "phenomenon":  "<text>",
  "score":       ""            # annotator will fill 1‒5
}
"""

from pathlib import Path
import importlib.util
import json, sys

# ---------------- paths -----------------
SERVER_FILE = Path("env_info.py")   # change to your file
OUTPUT_JSON = Path("annotation_table.json")
# ----------------------------------------

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

def load_lists(pyfile: Path):
    spec = importlib.util.spec_from_file_location("env_mod", pyfile)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    unsafe = getattr(mod, "Unsafe_env_info", None)
    safe   = getattr(mod, "Safe_env_info", None)
    if unsafe is None or safe is None:
        sys.exit("Lists Unsafe_env_info or Safe_env_info not found.")
    return unsafe, safe

def build_rows(unsafe, safe):
    rows = []
    for i, ph in enumerate(unsafe):
        rows.append({
            "id": len(rows)+1,
            "risk_type": RISK_TYPES[i // 10] if i < 100 else "unknown",
            "phenomenon": ph,
            "score": ""
        })
    for ph in safe:
        rows.append({
            "id": len(rows)+1,
            "risk_type": "safe",
            "phenomenon": ph,
            "score": ""
        })
    return rows

def main():
    unsafe, safe = load_lists(SERVER_FILE)
    rows = build_rows(unsafe, safe)
    OUTPUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Wrote {len(rows)} entries → {OUTPUT_JSON}")

if __name__ == "__main__":
    main()

