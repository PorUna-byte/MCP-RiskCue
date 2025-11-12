import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from openai import OpenAI

# python query_generator.py --desc_file serverDes_prin.json --query_file queries_prin.jsonl --max_workers 40 --temp_dir Temp
# python query_generator.py --desc_file serverDes_env.json --query_file queries_env.jsonl --max_workers 100 --temp_dir Temp
 
# -------------------- env & defaults --------------------
load_dotenv()

SYSTEM_PROMPT = """
You are a query generator helping to build an evaluation benchmark for large-language-model (LLM) tool use.

**Task**
Given the full signatures and docstrings of every tool offered by ONE MCP Server, write **exactly 50 distinct, natural-sounding user queries (in English)** that can be answered by calling those tools—either individually or in combination.

**Diversity requirements**
1. Vary intents, phrasing styles, and specificity.  
   • Mix short single-sentence requests with longer multi-sentence ones.  
   • Use first-person ("I …"), second-person ("Could you …"), imperative ("Give me …") and question forms.  
2. Cover the full parameter space: different values, typical defaults, uncommon but valid inputs.  
3. Include a spectrum of difficulty: straightforward look-ups, comparative questions, what-if scenarios, etc.  
4. Avoid trivial duplication—each query must be meaningfully different in goal or wording.  
5. Language must be clear, idiomatic **English**; no other languages or code snippets.
6. The queries MUST BE SOLVED IN LIMITED TIME, typically 6 seconds.

**Output rules**
• Return **only** the 12 queries, one per line, no numbering, no bullet marks, no commentary before or after.  
• Do not show tool signatures or explanations—produce just the queries themselves.
"""

API_KEY     = os.getenv("API_KEY")
BASE_URL    = os.getenv("BASE_URL")
MODEL       = os.getenv("MODEL") or "gpt-4o-mini"
TEMPERATURE = 0.7
MAX_RETRY   = 3

llm = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# -------------------- helpers --------------------
def build_prompt(tools: List[Dict]) -> str:
    blocks = [f"{t['signature']}\n{t['description']}\n" for t in tools]
    return "TOOLS:\n\n" + "\n---\n".join(blocks)

def chat(prompt: str):
    for attempt in range(1, MAX_RETRY + 1):
        try:
            return llm.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as e:
            print(f"[WARN] API error attempt {attempt}: {e}")
            if attempt == MAX_RETRY:
                raise
            time.sleep(2 ** attempt)

def save_intermediate_result(path: str, queries: List[str], temp_dir: Path):
    """Save intermediate result to temp file."""
    temp_file = temp_dir / f"{path.replace('/', '_')}.json"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump({"path": path, "queries": queries}, f, ensure_ascii=False, indent=2)

def load_intermediate_results(temp_dir: Path) -> Dict[str, List[str]]:
    """Load existing intermediate results from temp directory."""
    results = {}
    if not temp_dir.exists():
        return results
    
    for temp_file in temp_dir.glob("*.json"):
        try:
            with open(temp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                results[data["path"]] = data["queries"]
                print(f"   • Loaded checkpoint: {data['path']} (queries: {len(data['queries'])})")
        except Exception as e:
            print(f"[WARN] Failed to load checkpoint {temp_file}: {e}")
    
    return results

def _gen_for_server(item: Tuple[str, List[Dict]], temp_dir: Path):
    """Worker: given (path, tools) → (path, queries) and save to temp."""
    path, tools = item
    prompt_txt = build_prompt(tools)
    resp = chat(prompt_txt)
    text = (resp.choices[0].message.content or "").strip()
    queries = [q.strip() for q in text.splitlines() if q.strip()]
    
    # Save intermediate result immediately
    save_intermediate_result(path, queries, temp_dir)
    
    return path, queries

def write_jsonl_output(queries: Dict[str, List[str]], output_file: Path):
    """Write queries to JSONL format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for path, query_list in queries.items():
            for query in query_list:
                json.dump({"path": path, "query": query}, f, ensure_ascii=False)
                f.write('\n')

# -------------------- main --------------------
def main():
    parser = argparse.ArgumentParser(description="Generate queries concurrently.")
    parser.add_argument("--desc_file", required=True, help="Path to serverDes_prin.json")
    parser.add_argument("--query_file", required=True, help="Path to output queries_prin.jsonl")
    parser.add_argument("--max_workers", type=int, default=8, help="Thread pool size")
    parser.add_argument("--temp_dir", default="Temp", help="Directory for intermediate results")
    args = parser.parse_args()

    DESC_FILE = Path(args.desc_file)
    QUERY_FILE = Path(args.query_file)
    TEMP_DIR = Path(args.temp_dir)
    
    # Ensure temp directory exists
    TEMP_DIR.mkdir(exist_ok=True)

    servers: Dict[str, List[Dict]] = json.loads(DESC_FILE.read_text())
    
    # Load existing intermediate results
    print("→ Loading existing checkpoints...")
    out_queries = load_intermediate_results(TEMP_DIR)
    
    # Filter out already completed servers
    remaining_servers = {k: v for k, v in servers.items() if k not in out_queries}
    
    if remaining_servers:
        print(f"→ Resuming with {len(remaining_servers)} remaining servers, {args.max_workers} threads, MODEL={MODEL}")
        
        with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
            futures = {ex.submit(_gen_for_server, item, TEMP_DIR): item[0] for item in remaining_servers.items()}
            for fut in as_completed(futures):
                path = futures[fut]
                try:
                    p, queries = fut.result()
                    out_queries[p] = queries
                    print(f"   • Done: {p}  (queries: {len(queries)})")
                except Exception as e:
                    print(f"[ERROR] {path}: {e}")
                    out_queries[path] = []  # 保底写入
    else:
        print("→ All servers already completed, proceeding to output generation...")

    # Write final output in JSONL format
    write_jsonl_output(out_queries, QUERY_FILE)
    print(f"\n✓ Done. Wrote {sum(len(q) for q in out_queries.values())} queries → {QUERY_FILE}")
    
    # Optionally clean up temp files
    if input("\nClean up temporary files? (y/N): ").lower() == 'y':
        for temp_file in TEMP_DIR.glob("*.json"):
            temp_file.unlink()
        print("✓ Temporary files cleaned up")

if __name__ == "__main__":
    main()
