#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shuffle four @mcp.tool blocks (with their header comments) but keep
`if __name__ == "__main__": …` at the very end.
"""

from pathlib import Path
import random, re
from typing import List, Tuple

DEC_RE = re.compile(r'^\s*@mcp\.tool', re.I)
COMMENT_RE = re.compile(r'^\s*#')

# ---------------------------------------------------------------------
def split_blocks(code: str) -> Tuple[str, List[str], str]:
    """Return (preamble, tool_blocks[4], epilogue)."""
    lines = code.splitlines(keepends=True)
    dec_starts = []

    for i, ln in enumerate(lines):
        if DEC_RE.match(ln):
            # include contiguous comment line immediately above
            start = i
            if i > 0 and COMMENT_RE.match(lines[i-1]):
                start -= 1
            dec_starts.append(start)

    if len(dec_starts) != 4:
        raise ValueError(f"Need exactly 4 @mcp.tool decorators, found {len(dec_starts)}")

    # Compute slices
    blocks = []
    preamble = "".join(lines[:dec_starts[0]])

    for idx, s in enumerate(dec_starts):
        end = dec_starts[idx+1] if idx < 3 else None  # None → EOF
        block = "".join(lines[s:end])
        blocks.append(block)

    # epilogue begins right after last block
    last_end = dec_starts[-1]
    # advance to line after last block
    for j in range(last_end, len(lines)):
        if j == len(lines)-1 or DEC_RE.match(lines[j+1]):  # next deco or eof
            continue
    epilogue = "".join(lines[dec_starts[-1] + len(blocks[-1].splitlines(keepends=True)):])

    return preamble, blocks, epilogue


def shuffle_mcp_tools(src_dir: str | Path, dst_dir: str | Path, *, seed: int | None = None):
    """Shuffle tool blocks for each .py in src_dir and write to dst_dir."""
    src_dir, dst_dir = Path(src_dir), Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    for py in src_dir.glob("*.py"):
        text = py.read_text(encoding="utf-8")
        try:
            pre, blocks, epi = split_blocks(text)
        except ValueError as e:
            print(f"Skip {py.name}: {e}")
            continue

        rng.shuffle(blocks)
        shuffled = pre + "".join(blocks) + epi
        (dst_dir / py.name).write_text(shuffled, encoding="utf-8")
        print(f"✔ Shuffled {py.name}")


if __name__ == "__main__":
    shuffle_mcp_tools("Mislead_select", "Mislead_select_shuffled", seed=42)