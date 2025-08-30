#!/usr/bin/env python3
"""
分析脚本：分析所有env开头的评估结果文件
为不同模型创建比较图表，包括overall和各个类别的性能比较
"""

import json
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置图表样式
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def load_eval_results(directory_path: str):
    """
    加载所有env开头的评估结果文件
    """
    env_files = glob.glob(os.path.join(directory_path, "env_eval_results_*.jsonl"))
    
    results = {}
    for file_path in env_files:
        # 提取模型名称
        filename = os.path.basename(file_path)
        model_name = filename.replace("env_eval_results_", "").replace(".jsonl", "")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                results[model_name] = data
                print(f"成功加载: {model_name}")
        except Exception as e:
            print(f"加载文件 {file_path} 失败: {e}")
    
    return results


def calculate_metrics(tp, fp, fn, tn):
    """
    计算性能指标
    """
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / (tp + fp + fn + tn) if (tp + fp + fn + tn) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'accuracy': accuracy
    }


def plot_overall_comparison(results, output_dir):
    """
    绘制overall性能比较图 - 显示TP, FP, TN, FN原始数据
    """
    models = list(results.keys())
    
    # 获取overall原始数据
    overall_data = {}
    for model in models:
        overall = results[model]['overall']
        overall_data[model] = {
            'TP': overall['TP'],
            'FP': overall['FP'],
            'FN': overall['FN'],
            'TN': overall['TN']
        }
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Overall Performance Comparison Across Models (Raw Data)', fontsize=16, fontweight='bold')
    
    metrics_names = ['TP', 'FP', 'FN', 'TN']
    metric_labels = ['True Positives', 'False Positives', 'False Negatives', 'True Negatives']
    
    for i, (metric, label) in enumerate(zip(metrics_names, metric_labels)):
        ax = axes[i//2, i%2]
        
        values = [overall_data[model][metric] for model in models]
        bars = ax.bar(models, values, color=plt.cm.Set3(np.linspace(0, 1, len(models))))
        
        ax.set_title(f'{label}', fontweight='bold')
        ax.set_ylabel('Count')
        
        # 在柱状图上添加数值标签
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.01,
                   f'{value}', ha='center', va='bottom', fontsize=9)
        
        # 旋转x轴标签
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'overall_comparison.png'), dpi=300, bbox_inches='tight')
    plt.show()


def plot_category_comparison(results, output_dir):
    """
    为每个安全类别绘制性能比较图 - 显示TP, FP, TN, FN原始数据
    """
    # 获取所有类别
    first_model = list(results.keys())[0]
    categories = list(results[first_model]['per_type'].keys())
    
    for category in categories:
        print(f"正在绘制类别: {category}")
        
        models = list(results.keys())
        
        # 获取该类别的原始数据
        category_data = {}
        for model in models:
            if category in results[model]['per_type']:
                cat_data = results[model]['per_type'][category]
                category_data[model] = {
                    'TP': cat_data['TP'],
                    'FP': cat_data['FP'],
                    'FN': cat_data['FN'],
                    'TN': cat_data['TN']
                }
            else:
                # 如果某个模型没有该类别的数据，使用默认值
                category_data[model] = {
                    'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0
                }
        
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'{category} Performance Comparison Across Models (Raw Data)', fontsize=16, fontweight='bold')
        
        metrics_names = ['TP', 'FP', 'FN', 'TN']
        metric_labels = ['True Positives', 'False Positives', 'False Negatives', 'True Negatives']
        
        for i, (metric, label) in enumerate(zip(metrics_names, metric_labels)):
            ax = axes[i//2, i%2]
            
            values = [category_data[model][metric] for model in models]
            bars = ax.bar(models, values, color=plt.cm.Set3(np.linspace(0, 1, len(models))))
            
            ax.set_title(f'{label}', fontweight='bold')
            ax.set_ylabel('Count')
            
            # 在柱状图上添加数值标签
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.01,
                       f'{value}', ha='center', va='bottom', fontsize=9)
            
            # 旋转x轴标签
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 保存图表，文件名使用类别名称（去除特殊字符）
        safe_category_name = category.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
        plt.savefig(os.path.join(output_dir, f'{safe_category_name}_comparison.png'), dpi=300, bbox_inches='tight')
        plt.show()


def create_summary_table(results, output_dir):
    """
    创建汇总表格
    """
    models = list(results.keys())
    first_model = list(results.keys())[0]
    categories = ['overall'] + list(results[first_model]['per_type'].keys())
    
    # 创建汇总数据
    summary_data = []
    
    for model in models:
        model_data = {'Model': model}
        
        for category in categories:
            if category == 'overall':
                data = results[model]['overall']
            else:
                if category in results[model]['per_type']:
                    data = results[model]['per_type'][category]
                else:
                    data = {'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0}
            
            metrics = calculate_metrics(data['TP'], data['FP'], data['FN'], data['TN'])
            model_data[f'{category}_F1'] = f"{metrics['f1']:.3f}"
            model_data[f'{category}_Precision'] = f"{metrics['precision']:.3f}"
            model_data[f'{category}_Recall'] = f"{metrics['recall']:.3f}"
        
        summary_data.append(model_data)
    
    # 保存汇总数据
    summary_file = os.path.join(output_dir, 'summary_table.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"汇总表格已保存到: {summary_file}")
    
    return summary_data


def main():
    """
    主函数
    """
    # 设置目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, 'charts')
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    print("开始分析env评估结果...")
    
    # 加载所有结果
    results = load_eval_results(current_dir)
    
    if not results:
        print("没有找到任何env评估结果文件")
        return
    
    print(f"成功加载 {len(results)} 个模型的结果")
    print(f"模型列表: {list(results.keys())}")
    
    # 创建overall比较图
    print("\n正在创建overall性能比较图...")
    plot_overall_comparison(results, output_dir)
    
    # 创建各类别比较图
    print("\n正在创建各类别性能比较图...")
    plot_category_comparison(results, output_dir)
    
    # 创建汇总表格
    print("\n正在创建汇总表格...")
    summary_data = create_summary_table(results, output_dir)
    
    print(f"\n分析完成！所有图表已保存到: {output_dir}")
    
    # 打印简要统计
    print("\n=== 简要统计 ===")
    for model in results.keys():
        overall = results[model]['overall']
        metrics = calculate_metrics(overall['TP'], overall['FP'], overall['FN'], overall['TN'])
        print(f"{model}: F1={metrics['f1']:.3f}, Precision={metrics['precision']:.3f}, Recall={metrics['recall']:.3f}")


if __name__ == "__main__":
    main()
