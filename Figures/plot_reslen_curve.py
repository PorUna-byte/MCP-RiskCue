# -*- coding: utf-8 -*-
"""
Plot response-length curves (mean ± std) per model from reslen_curve.txt
- Larger fonts
- Save as PNG and PDF
Usage:
    python plot_reslen.py  # 默认读取 ./reslen_curve.txt
    # 或
    python plot_reslen.py /path/to/reslen_curve.txt
"""

import sys
import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ========== I/O ==========
in_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./reslen_curve.txt")
if not in_path.exists():
    raise FileNotFoundError(f"Input file not found: {in_path}")

out_png = in_path.with_suffix("")  # e.g. ./reslen_curve
out_png = Path(str(out_png) + "_fig.png")
out_pdf = Path(str(in_path.with_suffix("")) + "_fig.pdf")

# ========== Parse ==========
# 模型名行形如： "模型: Qwen-xxx"
header_re = re.compile(r"^\s*模型\s*:\s*(.+?)\s*$")

# 数据行示例（允许空格或制表符分隔）：
# Step  Mean  Std  Count  Mean±Std
# 100   34.2  3.1  50     34.2±3.1  （也兼容 34.2+/-3.1）
row_re = re.compile(
    r"^\s*(\d+)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+(\d+)\s+([+-]?\d+(?:\.\d+)?)(?:±|\+/-)([+-]?\d+(?:\.\d+)?)\s*$"
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
            continue  # 还没遇到模型名时的杂项行

        # 跳过分隔线或表头
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
            # m.group(5), m.group(6) 是 mean±std 的冗余展示，这里不用
            models[current_model].append(
                {"Model": current_model, "Step": step, "Mean": mean, "Std": std, "Count": cnt}
            )

# 组装 DataFrame
dfs = []
for model, rows in models.items():
    if rows:
        df = pd.DataFrame(rows)
        # 强制数值类型并按 Step 排序
        for col in ["Step", "Mean", "Std", "Count"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["Step", "Mean", "Std"]).sort_values("Step")
        dfs.append(df)

if not dfs:
    raise RuntimeError("未解析到有效数据行，请检查文本格式。")

all_df = pd.concat(dfs, ignore_index=True)

# ========== Plot (bigger fonts, single figure) ==========
plt.rcParams.update({
    "font.size": 14,        # 基础字号更大
    "axes.titlesize": 20,   # 标题
    "axes.labelsize": 16,   # 坐标轴标题
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
})

fig = plt.figure(figsize=(11, 7))  # 单图，不用子图；不手动设定颜色
ax = plt.gca()

for model, df in all_df.groupby("Model"):
    x = df["Step"].to_numpy(dtype=float)
    y = df["Mean"].to_numpy(dtype=float)
    s = df["Std"].to_numpy(dtype=float)

    ax.plot(x, y, label=model)                         # 均值曲线
    ax.fill_between(x, y - s, y + s, alpha=0.20)       # ±1 标准差阴影

ax.set_xlabel("Step")
ax.set_ylabel("Response Length")
ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
ax.legend(loc="best")
fig.tight_layout()

# ========== Save ==========
fig.savefig(out_png, dpi=220, bbox_inches="tight")
fig.savefig(out_pdf, bbox_inches="tight")
print(f"Saved: {out_png}")
print(f"Saved: {out_pdf}")


