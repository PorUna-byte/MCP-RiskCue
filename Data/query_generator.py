#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 50 user queries for each MCP Server & track OpenAI API cost.
"""

import json, os, time
from pathlib import Path
from openai import OpenAI
import openai
from dotenv import load_dotenv

# ---------- 配 置 ----------
TEMPERATURE = 0.7
MAX_RETRY = 3
SYSTEM_PROMPT = """
You are a dataset generator helping to build an evaluation benchmark for large-language-model (LLM) tool use.

**Task**
Given the full signatures and docstrings of every tool offered by ONE MCP Server, write **exactly 50 distinct, natural-sounding user queries (in English)** that can be answered by calling those tools—either individually or in combination.

**Diversity requirements**
1. Vary intents, phrasing styles, and specificity.  
   • Mix short single-sentence requests with longer multi-sentence ones.  
   • Use first-person (“I …”), second-person (“Could you …”), imperative (“Give me …”) and question forms.  
2. Cover the full parameter space: different values, edge cases, typical defaults, uncommon but valid inputs.  
3. Include a spectrum of difficulty: straightforward look-ups, comparative questions, what-if scenarios, error-handling or boundary conditions, etc.  
4. Avoid trivial duplication—each query must be meaningfully different in goal or wording.  
5. Language must be clear, idiomatic **English**; no other languages or code snippets.

**Output rules**
• Return **only** the 50 queries, one per line, no numbering, no bullet marks, no commentary before or after.  
• Do not show tool signatures or explanations—produce just the queries themselves.
"""

# 价格表：美元 / 1K tokens
PRICE = {
    "gpt-4o-mini": dict(prompt=0.00060, completion=0.00240),  # per 1 K tokens
    "gpt-4o":      dict(prompt=0.00500, completion=0.02000),
    "o3": dict(prompt=0.002, completion=0.008)
}
# ---------------------------

ROOT         = Path(__file__).resolve().parent
DESC_FILE    = ROOT / "serverDes_prin.json"
QUERY_FILE   = ROOT / "queries_prin.json"
COST_FILE    = ROOT / "queries_cost.json"

load_dotenv()
llm = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)
MODEL = os.getenv('MODEL')

def build_prompt(tools):
    blocks = [f"{t['signature']}\n{t['description']}\n" for t in tools]
    return "TOOLS:\n\n" + "\n---\n".join(blocks)

def chat(prompt):
    for attempt in range(1, MAX_RETRY + 1):
        try:
            resp = llm.chat.completions.create(
                model=os.getenv("MODEL"),
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )
            return resp
        except Exception as e:
            print(f"[WARN] API error attempt {attempt}: {e}")
            if attempt == MAX_RETRY:
                raise
            time.sleep(2 ** attempt)

def main():
    servers = json.loads(DESC_FILE.read_text())
    out_queries, cost_breakdown = {}, {"total_tokens": 0, "total_usd": 0, "details": {}}

    for path, tools in servers.items():
        print(f"→ Generating for {path}")
        prompt_txt = build_prompt(tools)
        resp = chat(prompt_txt)

        text = resp.choices[0].message.content.strip()
        queries = [q for q in text.splitlines() if q.strip()]
        out_queries[path] = queries

        # ---- 计费 ----
        usage = resp.usage  # openai 1.x: .usage.prompt_tokens / completion_tokens
        p_tok, c_tok = usage.prompt_tokens, usage.completion_tokens
        price_prompt = p_tok / 1000 * PRICE[MODEL]["prompt"]
        price_completion = c_tok / 1000 * PRICE[MODEL]["completion"]
        total_cost = price_prompt + price_completion

        cost_breakdown["total_tokens"] += p_tok + c_tok
        cost_breakdown["total_usd"] += total_cost
        cost_breakdown["details"][path] = {
            "prompt_tokens": p_tok,
            "completion_tokens": c_tok,
            "cost_usd": round(total_cost, 6),
        }

        #增量保存
        QUERY_FILE.write_text(json.dumps(out_queries, indent=2, ensure_ascii=False))
        # COST_FILE.write_text(json.dumps(cost_breakdown, indent=2, ensure_ascii=False))

    print(f"\n✓ Done. Total tokens: {cost_breakdown['total_tokens']}, "
          f"Total cost: ${cost_breakdown['total_usd']:.6f}")
    print(f"Queries → {QUERY_FILE}\nCost report → {COST_FILE}")

if __name__ == "__main__":
    main()