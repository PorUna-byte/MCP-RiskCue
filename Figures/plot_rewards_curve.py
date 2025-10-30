# -*- coding: utf-8 -*-
"""
Plot rewards curves (mean ± std) per model from rewards_curve.txt
- Larger fonts
- Save as PNG and PDF

Usage:
    python plot_rewards.py            # 默认读取 ./rewards_curve.txt
    python plot_rewards.py /path/to/rewards_curve.txt
"""

import sys
import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ======== I/O ========
in_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./rewards_curve.txt")
if not in_path.exists():
    raise FileNotFoundError(f"Input file not found: {in_path}")

out_png = Path(str(in_path.with_suffix("")) + "_fig.png")
out_pdf = Path(str(in_path.with_suffix("")) + "_fig.pdf")

# ======== Parse ========
# 模型名行：例如 "模型: Llama-Guard-3-8B"
header_re = re.compile(r"^\s*模型\s*:\s*(.+?)\s*$")

# 数据行：Step  Mean  Std  Count  Mean±Std（也兼容 +/− 写法）
row_re = re.compile(
    r"^\s*(\d+)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+(\d+)\s+"
    r"([+-]?\d+(?:\.\d+)?)(?:±|\+/-)([+-]?\d+(?:\.\d+)?)\s*$"
)

models = {}
current_model = None

with in_path.open("r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line:
            continue

        m = header_re.match(line)
        if m:
            current_model = m.group(1).strip()
            models[current_model] = []
            continue

        if current_model is None:
            continue  # 还未遇到“模型:”行前的内容

        # 跳过分隔线/表头
        if set(line) <= set("=-*—_ \t"):
            continue
        if line.split()[0].lower() in {"step", "mean", "std", "count"}:
            continue

        m = row_re.match(line)
        if m:
            step = int(m.group(1))
            mean = float(m.group(2))
            std  = float(m.group(3))
            cnt  = int(m.group(4))
            models[current_model].append(
                {"Model": current_model, "Step": step, "Mean": mean, "Std": std, "Count": cnt}
            )

# 合并为 DataFrame
dfs = []
for model, rows in models.items():
    if rows:
        df = pd.DataFrame(rows)
        for col in ["Step", "Mean", "Std", "Count"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["Step", "Mean", "Std"]).sort_values("Step")
        dfs.append(df)

if not dfs:
    raise RuntimeError("未解析到有效数据行，请检查文本格式。")

all_df = pd.concat(dfs, ignore_index=True)

# ======== Plot (bigger fonts) ========
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 20,
    "axes.labelsize": 16,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
})

fig = plt.figure(figsize=(11, 7))
ax = plt.gca()

for model, df in all_df.groupby("Model"):
    x = df["Step"].to_numpy(dtype=float)
    y = df["Mean"].to_numpy(dtype=float)
    s = df["Std"].to_numpy(dtype=float)

    ax.plot(x, y, label=model)                 # 均值曲线（不同模型自动不同颜色）
    ax.fill_between(x, y - s, y + s, alpha=0.20)  # ±1 标准差阴影

ax.set_xlabel("Step")
ax.set_ylabel("Reward")
ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
ax.legend(loc="best")
fig.tight_layout()

# ======== Save ========
fig.savefig(out_png, dpi=220, bbox_inches="tight")
fig.savefig(out_pdf, bbox_inches="tight")
print(f"Saved: {out_png}")
print(f"Saved: {out_pdf}")