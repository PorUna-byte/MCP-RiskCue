import pandas as pd
import numpy as np

# 读取三个文件
file_paths = ["reslen_r1.csv", "reslen_r2.csv", "reslen_r3.csv"]
dfs = []
for file_path in file_paths:
    df = pd.read_csv(file_path)
    dfs.append(df)

# 获取所有模型名称
step_col = "eval/step"
reslen_cols = [c for c in dfs[0].columns if "eval/MCPenv_response_lengths" in c and "__" not in c]

# 提取模型名称
model_names = []
for col in reslen_cols:
    model_name = col.split(" - ")[0].split("_")[0]
    if model_name not in model_names:
        model_names.append(model_name)

print(f"找到的模型: {model_names}")

# 为每个模型计算统计量
model_stats = {}
for model_name in model_names:
    print(f"处理模型: {model_name}")
    
    # 收集该模型在三个文件中的数据
    model_data = []
    steps_data = []
    
    for df in dfs:
        # 找到该模型对应的列
        model_col = None
        for col in df.columns:
            if model_name in col and "eval/MCPenv_response_lengths" in col and "__" not in col:
                model_col = col
                break
        
        if model_col is not None:
            model_data.append(df[model_col].values)
            steps_data.append(df[step_col].values)
    
    if len(model_data) > 0:
        # 找到最大长度
        max_length = max(len(data) for data in model_data)
        
        # 为每个步骤计算统计量
        step_stats = []
        
        for step_idx in range(max_length):
            # 收集该步骤所有可用的response_lengths值
            step_lengths = []
            step_values = []
            
            for i, data in enumerate(model_data):
                if step_idx < len(data) and pd.notna(data[step_idx]):
                    step_lengths.append(data[step_idx])
                    step_values.append(steps_data[i][step_idx])
            
            # 计算该步骤的统计量
            if len(step_lengths) > 0:
                step_stats.append({
                    'step': step_values[0] if len(step_values) > 0 else step_idx * 20,
                    'mean': np.mean(step_lengths),
                    'std': np.std(step_lengths),
                    'count': len(step_lengths)
                })
        
        model_stats[model_name] = step_stats

# 输出到文件
with open("reslen_curve.txt", "w", encoding="utf-8") as f:
    f.write("=== 每个模型在三次实验中每个步骤的Response Length统计 ===\n\n")
    
    for model_name, stats in model_stats.items():
        f.write(f"模型: {model_name}\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Step':<8} {'Mean':<12} {'Std':<12} {'Count':<8} {'Mean±Std':<20}\n")
        f.write("-" * 80 + "\n")
        
        for stat in stats:
            step = stat['step']
            mean = stat['mean']
            std = stat['std']
            count = stat['count']
            mean_std_str = f"{mean:.6f}±{std:.6f}"
            
            f.write(f"{step:<8} {mean:<12.6f} {std:<12.6f} {count:<8} {mean_std_str:<20}\n")
        
        f.write("\n" + "="*100 + "\n\n")

print("✅ 统计结果已保存到 reslen_curve.txt")

# 同时打印到控制台
print("\n=== 每个模型在三次实验中每个步骤的Response Length统计 ===\n")

for model_name, stats in model_stats.items():
    print(f"模型: {model_name}")
    print("-" * 80)
    print(f"{'Step':<8} {'Mean':<12} {'Std':<12} {'Count':<8} {'Mean±Std':<20}")
    print("-" * 80)
    
    for stat in stats:
        step = stat['step']
        mean = stat['mean']
        std = stat['std']
        count = stat['count']
        mean_std_str = f"{mean:.6f}±{std:.6f}"
        
        print(f"{step:<8} {mean:<12.6f} {std:<12.6f} {count:<8} {mean_std_str:<20}")
    
    print("\n" + "="*100 + "\n")
