#!/usr/bin/env python3
"""
统计脚本：分析histories_env.jsonl和histories_prin.jsonl中每条数据的history长度
统计不同token长度范围的数据数量，并将超过2048个token的数据保存到overlong.jsonl中
"""

import json
import re
import os
from collections import defaultdict
from typing import Dict, List, Tuple
from transformers import AutoTokenizer
from pathlib import Path

ck_dir = "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints"


def count_tokens(text: str, tokenizer=None) -> int:
    """
    使用Gemma2-2b tokenizer计算token数量
    """
    if tokenizer is None:
        return 0
    
    try:
        # 使用tokenizer计算token数量
        tokens = tokenizer.encode(text, add_special_tokens=False)
        return len(tokens)
    except Exception as e:
        print(f"Warning: tokenizer计算失败: {e}")
        # 如果tokenizer失败，回退到简单的字符计数
        return len(text.split())


def analyze_history_length(history: List[Dict], tokenizer=None) -> int:
    """
    计算history中所有消息的token总数
    """
    total_tokens = 0
    
    for message in history:
        if isinstance(message, dict) and 'content' in message:
            content = message['content']
            if isinstance(content, str):
                total_tokens += count_tokens(content, tokenizer)
    
    return total_tokens


def process_jsonl_file(file_path: str, tokenizer=None) -> Tuple[List[int], List[Dict]]:
    """
    处理JSONL文件，返回所有history的token长度和超过2048的数据
    """
    token_lengths = []
    overlong_data = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    
                    if 'history' in data and isinstance(data['history'], list):
                        token_count = analyze_history_length(data['history'], tokenizer)
                        token_lengths.append(token_count)
                        
                        # 如果超过2048个token，保存到overlong_data
                        if token_count > 2048:
                            overlong_data.append({
                                'file': file_path,
                                'line': line_num,
                                'token_count': token_count,
                                'data': data
                            })
                    
                except json.JSONDecodeError as e:
                    print(f"Warning: 第{line_num}行JSON解析失败: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 不存在")
        return [], []
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")
        return [], []
    
    return token_lengths, overlong_data


def categorize_by_token_ranges(token_lengths: List[int]) -> Dict[str, int]:
    """
    按token长度范围分类统计
    """
    categories = {
        "0-1024": 0,
        "1024-2048": 0,
        ">2048": 0
    }
    
    for length in token_lengths:
        if length <= 1024:
            categories["0-1024"] += 1
        elif length <= 2048:
            categories["1024-2048"] += 1
        else:
            categories[">2048"] += 1
    
    return categories


def save_overlong_data(overlong_data: List[Dict], output_file: str = "overlong.jsonl"):
    """
    保存超过2048个token的数据到JSONL文件
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in overlong_data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
        print(f"已将 {len(overlong_data)} 条超过2048个token的数据保存到 {output_file}")
    except Exception as e:
        print(f"保存overlong数据时发生错误: {e}")


def print_statistics(file_name: str, token_lengths: List[int], categories: Dict[str, int]):
    """
    打印统计信息
    """
    print(f"\n=== {file_name} 统计结果 ===")
    print(f"总数据条数: {len(token_lengths)}")
    
    if token_lengths:
        print(f"最小token数: {min(token_lengths)}")
        print(f"最大token数: {max(token_lengths)}")
        print(f"平均token数: {sum(token_lengths) / len(token_lengths):.2f}")
        
        # 按范围统计
        print("\n按token长度范围统计:")
        for range_name, count in categories.items():
            percentage = (count / len(token_lengths)) * 100
            print(f"  {range_name}: {count} 条 ({percentage:.1f}%)")


def main():
    """
    主函数
    """
    print("开始分析JSONL文件中的history长度...")
    
    # 初始化Gemma2-2b tokenizer
    print("正在加载Gemma2-2b tokenizer...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(os.path.join(ck_dir, 'Gemma-2-2B'))
        print("Tokenzier加载成功！")
    except Exception as e:
        print(f"Warning: 无法加载Gemma2-2b tokenizer: {e}")
        print("将使用简单的字符计数方法作为备选")
        tokenizer = None
    
    # 要分析的文件列表
    files_to_analyze = [
        "histories_env.jsonl",
        "histories_prin.jsonl"
    ]
    
    all_token_lengths = []
    all_overlong_data = []
    
    # 处理每个文件
    for file_path in files_to_analyze:
        print(f"\n正在处理文件: {file_path}")
        
        token_lengths, overlong_data = process_jsonl_file(file_path, tokenizer)
        
        if token_lengths:
            categories = categorize_by_token_ranges(token_lengths)
            print_statistics(file_path, token_lengths, categories)
            
            all_token_lengths.extend(token_lengths)
            all_overlong_data.extend(overlong_data)
        else:
            print(f"文件 {file_path} 没有有效数据或处理失败")
    
    # 汇总统计
    if all_token_lengths:
        print("\n" + "="*50)
        print("=== 汇总统计 ===")
        
        total_categories = categorize_by_token_ranges(all_token_lengths)
        print_statistics("所有文件汇总", all_token_lengths, total_categories)
        
        # 保存超过2048个token的数据
        if all_overlong_data:
            save_overlong_data(all_overlong_data)
        else:
            print("没有发现超过2048个token的数据")
    else:
        print("没有找到有效数据进行统计")


if __name__ == "__main__":
    main()
