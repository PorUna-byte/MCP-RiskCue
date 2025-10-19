import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ========== 数据定义 ==========
train_data = {
    "Sensitive Data Exfiltration": {"Count": 195, "Unique Observations": 77},
    "Covert Channel Attack": {"Count": 215, "Unique Observations": 80},
    "Malicious Code Execution": {"Count": 215, "Unique Observations": 76},
    "Privilege Escalation": {"Count": 187, "Unique Observations": 77},
    "Persistence via Backdoor Implantation": {"Count": 202, "Unique Observations": 76},
    "Cache or Local State Pollution": {"Count": 210, "Unique Observations": 78},
    "Delayed or Time-Triggered Attacks": {"Count": 208, "Unique Observations": 76},
    "Denial-of-Service": {"Count": 215, "Unique Observations": 77},
    "Log Explosion Attacks": {"Count": 205, "Unique Observations": 76},
    "Safe": {"Count": 681, "Unique Observations": 666},
}

test_data = {
    "Sensitive Data Exfiltration": {"Count": 48, "Unique Observations": 20},
    "Covert Channel Attack": {"Count": 30, "Unique Observations": 20},
    "Malicious Code Execution": {"Count": 42, "Unique Observations": 18},
    "Privilege Escalation": {"Count": 38, "Unique Observations": 20},
    "Persistence via Backdoor Implantation": {"Count": 38, "Unique Observations": 19},
    "Cache or Local State Pollution": {"Count": 28, "Unique Observations": 19},
    "Delayed or Time-Triggered Attacks": {"Count": 36, "Unique Observations": 19},
    "Denial-of-Service": {"Count": 39, "Unique Observations": 20},
    "Log Explosion Attacks": {"Count": 32, "Unique Observations": 20},
    "Safe": {"Count": 170, "Unique Observations": 169},
}

# 顺序与编号
risk_order = [
    "Sensitive Data Exfiltration",
    "Covert Channel Attack",
    "Malicious Code Execution",
    "Privilege Escalation",
    "Persistence via Backdoor Implantation",
    "Cache or Local State Pollution",
    "Delayed or Time-Triggered Attacks",
    "Denial-of-Service",
    "Log Explosion Attacks",
    "Safe",
]
circle_labels = ["①","②","③","④","⑤","⑥","⑦","⑧","⑨","Safe"]

# 辅助函数
def dict_to_df(data_dict, order):
    rows = []
    for k in order:
        v = data_dict[k]
        rows.append({"Risk Type": k, "Count": v["Count"], "Unique Observations": v["Unique Observations"]})
    return pd.DataFrame(rows)

df_train = dict_to_df(train_data, risk_order)
df_test = dict_to_df(test_data,  risk_order)

def plot_and_save(df, title, filename_prefix):
    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(df))
    bar_w = 0.42

    ax.bar(x - bar_w/2, df["Count"].values, width=bar_w, label="Total Counts")
    ax.bar(x + bar_w/2, df["Unique Observations"].values, width=bar_w, label="Unique Counts")

    ax.set_xticks(x)
    ax.set_xticklabels(circle_labels, fontsize=28)
    ax.set_ylabel("Number", fontsize=24)
    ax.set_xlabel("Risk Types", fontsize=24)
    ax.tick_params(axis='y', labelsize=18)  # 设置y轴刻度数字的字体大小
    ax.legend(fontsize=24)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()

    # 保存 PNG 和 PDF
    plt.savefig(f"{filename_prefix}.png", dpi=300)
    plt.savefig(f"{filename_prefix}.pdf", dpi=300)
    plt.show()

# 绘制并保存
plot_and_save(df_train, "Total Counts and Unique System Logs For Each Risk Type", "env_data_train_risk_stats")
plot_and_save(df_test,  "Total Counts and Unique System Logs For Each Risk Type", "env_data_test_risk_stats")

# 输出统计表
obs_stats = pd.DataFrame(
    {
        "File": ["env_data_train.jsonl", "env_data_test.jsonl"],
        "Max Occurrences": [3, 3],
        "Min Occurrences": [1, 1],
        "Median": [2.00, 1.00],
        "Mean": [1.84, 1.45],
    }
)
print("\nObservation Occurrence Statistics:")
print(obs_stats.to_string(index=False))

# 编号映射表
mapping_df = pd.DataFrame({"Circle": circle_labels, "Risk Type": risk_order})
print("\nLegend (Circle → Risk Type):")
print(mapping_df.to_string(index=False))
