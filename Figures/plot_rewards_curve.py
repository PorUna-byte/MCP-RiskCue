import pandas as pd
import matplotlib.pyplot as plt

# ========== 1. 读取文件 ==========
file_path = "rewards_curve.csv"
df = pd.read_csv(file_path)

# ========== 2. 筛选所需列 ==========
step_col = "eval/step"
reward_cols = [c for c in df.columns if "eval/MCPenv_rewards" in c and "__" not in c]

# ========== 3. 绘图配置 ==========
plt.figure(figsize=(9, 6))
colors = plt.get_cmap("tab10").colors  # 高区分度调色板

# 绘制每个模型的曲线
for i, col in enumerate(reward_cols):
    model_name = col.split(" - ")[0].split("_")[0]  # 去掉 _ 后缀
    plt.plot(
        df[step_col],
        df[col],
        label=model_name,
        color=colors[i % len(colors)],
        linewidth=2.2
    )

# ========== 4. 样式与字体 ==========
plt.xlabel("step", fontsize=16)
plt.ylabel("Rewards", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14, loc='lower right')
plt.grid(alpha=0.3, linewidth=0.8)
plt.tight_layout()

# ========== 5. 保存图像 ==========
plt.savefig("MCPenv_rewards_curve.pdf", dpi=300)
plt.savefig("MCPenv_rewards_curve.png", dpi=300)

plt.show()
print("✅ 图像已导出：MCPenv_rewards_curve.pdf 与 MCPenv_rewards_curve.png")
