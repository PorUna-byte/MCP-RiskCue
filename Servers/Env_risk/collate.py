#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robustly collect function signatures & full docstrings across project, even if
some .py files contain syntax errors.

Usage
-----
python collect_server_descriptions.py
"""

from pathlib import Path
from textwrap import dedent
import ast, json, datetime, sys

ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / "serverDes_env.json"
THIS_FILE = Path(__file__).resolve()          # ← 当前脚本绝对路径

def build_signature(func: ast.FunctionDef) -> str:
    """Reconstruct a readable function signature from AST."""
    args = []
    # align defaults list to args length
    defaults = [None] * (len(func.args.args) - len(func.args.defaults)) + func.args.defaults
    for arg_node, default in zip(func.args.args, defaults):
        part = arg_node.arg
        if arg_node.annotation:
            part += f": {ast.unparse(arg_node.annotation).strip()}"
        if default:
            part += f" = {ast.unparse(default).strip()}"
        args.append(part)

    if func.args.vararg:
        args.append(f"*{func.args.vararg.arg}")
    if func.args.kwarg:
        args.append(f"**{func.args.kwarg.arg}")

    ret = ast.unparse(func.returns).strip() if func.returns else ""
    signature = f"def {func.name}({', '.join(args)})"
    return f"{signature} -> {ret}" if ret else signature


def extract_from_file(py_path: Path):
    """Return list of {'signature', 'description'} dicts for a given .py file."""
    try:
        source = py_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(py_path))
    except (SyntaxError, UnicodeDecodeError) as exc:
        # Bubble up the path & error message to caller for logging
        raise RuntimeError(f"{py_path}: {exc}") from None

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(
                {
                    "signature": build_signature(node),
                    "description": dedent(ast.get_docstring(node) or "").strip(),
                }
            )
    return functions

def main():
    collected = {}
    failed_files = []

    for py_file in ROOT.rglob("*.py"):
        # 1) 跳过 __init__.py
        if py_file.name == "__init__.py":
            continue
        # 2) 跳过本脚本自身
        if py_file.resolve() == THIS_FILE:
            continue

        try:
            funcs = extract_from_file(py_file)
            if funcs:
                collected[py_file.relative_to(ROOT).as_posix()] = funcs
        except RuntimeError as err:
            failed_files.append(str(err))

    OUTPUT_FILE.write_text(json.dumps(collected, indent=2, ensure_ascii=False), "utf-8")
    print(f"✔ Parsed {sum(len(v) for v in collected.values())} functions "
          f"from {len(collected)} files → {OUTPUT_FILE}")

    if failed_files:
        print("\n⚠️  The following files were skipped due to parse errors:")
        for msg in failed_files:
            print("   -", msg)
        print(f"Total skipped files: {len(failed_files)}")


if __name__ == "__main__":
    main()
