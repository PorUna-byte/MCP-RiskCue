#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filter a JSON dataset of MCP‑server interactions.

Input  (JSON)
-------------
A dict that maps each MCP‑server file (path) to a list of items.  
Each item is a dict: { "query": <str>, "response": <list> }.

Filtering rules
---------------
1. Drop items whose query == "<FILLER QUERY>" (exact match).
2. Drop items whose response list:
   • is not length 5, OR
   • does not have roles == ["system","user","assistant","assistant","assistant"].

Output (JSON)
-------------
A dict mapping the MCP‑server name (same keys as input) to a list of **kept
query strings**.

Author: 2025‑07‑19
"""

from pathlib import Path
import json, sys
A1_OLD = "This is MCP tool-call message:"
A1_NEW = "MCP tool-call message:"



# ----------------------------------------------------------------------
# Config: change paths as needed
# ----------------------------------------------------------------------
INPUT_PATH  = Path("histories_env.json")
QUERY_OUTPUT_PATH = Path("queries_env_filtered.json")
HISTORY_OUTPUT_PATH = Path("histories_env_filtered.json")

# ----------------------------------------------------------------------
# Helper: validate response structure
# ----------------------------------------------------------------------

def is_valid_response(resp_list):
    EXPECTED_ROLES = ["system", "user", "assistant", "assistant", "assistant","assistant"]
    """Return True if resp_list matches the required structure."""
    if not isinstance(resp_list, list) or len(resp_list) < 5:
        return False
    for elem, role in zip(resp_list[:5], EXPECTED_ROLES):
        if not isinstance(elem, dict) or elem.get("role") != role:
            return False
    return True


def modify_response(resp_list):
    if resp_list[2]["content"].startswith(A1_OLD):
            resp_list[2]["content"] = resp_list[2]["content"].replace(A1_OLD, A1_NEW, 1)

    return resp_list

# ----------------------------------------------------------------------
# Main filter‑and‑group pipeline
# ----------------------------------------------------------------------
def main():
    # 1) Load input
    try:
        data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"❌ Input file not found: {INPUT_PATH}")
    except json.JSONDecodeError as exc:
        sys.exit(f"❌ JSON parse error: {exc}")

    # 2) Iterate + filter
    grouped_queries = {}
    grouped_histories = {}

    for server_name, items in data.items():
        query_kept = []
        history_kept = []

        for item in items:
            query = item.get("query", "")
            histories = item.get("history", [])
            security_type = item.get("security_type", [])

            if query == "<FILLER QUERY>" or query=="":
                continue
            if not is_valid_response(histories):
                continue
            if len(security_type)==0:
                continue

            history = modify_response(histories)
            query_kept.append(query)
            history_kept.append({"query":query, "history":history, "security_type": security_type})

        if query_kept:
            grouped_queries[server_name] = query_kept
        if history_kept:
            grouped_histories[server_name] = history_kept


    # 3) Save output
    QUERY_OUTPUT_PATH.write_text(json.dumps(grouped_queries, ensure_ascii=False, indent=2), encoding="utf-8")
    HISTORY_OUTPUT_PATH.write_text(json.dumps(grouped_histories, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Saved {sum(len(v) for v in grouped_queries.values())} queries "
          f"from {len(grouped_queries)} servers to {QUERY_OUTPUT_PATH}")

    print(f"✅ Saved {sum(len(v) for v in grouped_histories.values())} histories "
          f"from {len(grouped_histories)} servers to {HISTORY_OUTPUT_PATH}")

if __name__ == "__main__":
    main()