#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collect the *first* function in each .py file that is decorated with
`@mcp.tool(...)`, together with its signature and full doc‑string.

Usage
-----
python collect_server_descriptions.py
"""

from pathlib import Path
from textwrap import dedent
import ast, json, datetime, sys

ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / "serverDes_prin.json"
THIS_FILE = Path(__file__).resolve()          # path of this collector script


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def build_signature(func: ast.FunctionDef) -> str:
    """Reconstruct a readable function signature from AST."""
    args = []
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
    sig = f"def {func.name}({', '.join(args)})"
    return f"{sig} -> {ret}" if ret else sig


def has_mcp_tool_decorator(func: ast.FunctionDef) -> bool:
    """Return True if the function has a decorator of the form @mcp.tool(...)."""
    for deco in func.decorator_list:
        # handle both @mcp.tool and @mcp.tool(...)
        target = deco.func if isinstance(deco, ast.Call) else deco
        if isinstance(target, ast.Attribute) and target.attr == "tool":
            if isinstance(target.value, ast.Name) and target.value.id == "mcp":
                return True
    return False


def extract_first_mcp_tool(py_path: Path):
    """Return {'signature', 'description'} or None for the first @mcp.tool func."""
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"), filename=str(py_path))
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"{py_path}: {exc}") from None

    for node in tree.body:                       # keep declaration order
        if isinstance(node, ast.FunctionDef) and has_mcp_tool_decorator(node):
            return [{
                "signature": build_signature(node),
                "description": dedent(ast.get_docstring(node) or "").strip(),
            }]
    return None


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    collected, failed = {}, []

    for file in ROOT.rglob("*.py"):
        if file.name == "__init__.py" or file.resolve() == THIS_FILE:
            continue

        try:
            entry = extract_first_mcp_tool(file)
            if entry:
                collected[file.relative_to(ROOT).as_posix()] = entry
        except RuntimeError as err:
            failed.append(str(err))

    OUTPUT_FILE.write_text(json.dumps(collected, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✔ Saved {len(collected)} entries to {OUTPUT_FILE}")

    if failed:
        print("\n⚠️  Skipped files due to parse errors:")
        for msg in failed:
            print("   -", msg)
        print(f"Total skipped: {len(failed)}")


if __name__ == "__main__":
    main()