#!/usr/bin/env python3
"""
数据清理脚本
删除overlong.jsonl中出现的重复数据，同时从histories_env.jsonl和queries_env.jsonl中删除对应数据
"""

import json
import os
from typing import Set, Dict, Any

def load_jsonl_file(file_path: str) -> list:
    """加载JSONL文件"""
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        item['_line_number'] = line_num  # 保存行号用于调试
                        data.append(item)
                    except json.JSONDecodeError as e:
                        print(f"警告: 第{line_num}行JSON解析失败: {e}")
                        continue
    return data

def save_jsonl_file(file_path: str, data: list):
    """保存数据到JSONL文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            # 移除调试用的行号
            if '_line_number' in item:
                del item['_line_number']
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def extract_queries_from_overlong(overlong_data: list) -> Set[str]:
    """从overlong数据中提取需要删除的查询"""
    queries_to_delete = set()
    
    for item in overlong_data:
        if 'data' in item and 'query' in item['data']:
            query = item['data']['query']
            queries_to_delete.add(query)
            print(f"标记删除查询: {query[:100]}...")
    
    return queries_to_delete

def clean_histories_file(histories_data: list, queries_to_delete: Set[str]) -> tuple[list, int]:
    """清理histories_env.jsonl文件"""
    cleaned_data = []
    deleted_count = 0
    
    for item in histories_data:
        if 'query' in item:
            query = item['query']
            if query in queries_to_delete:
                print(f"删除histories中的记录: {query[:100]}...")
                deleted_count += 1
                continue
        
        cleaned_data.append(item)
    
    return cleaned_data, deleted_count

def clean_queries_file(queries_data: list, queries_to_delete: Set[str]) -> tuple[list, int]:
    """清理queries_env.jsonl文件"""
    cleaned_data = []
    deleted_count = 0
    
    for item in queries_data:
        if 'query' in item:
            query = item['query']
            if query in queries_to_delete:
                print(f"删除queries中的记录: {query[:100]}...")
                deleted_count += 1
                continue
        
        cleaned_data.append(item)
    
    return cleaned_data, deleted_count

def main():
    """主函数"""
    print("开始数据清理...")
    
    # 文件路径
    overlong_file = "overlong.jsonl"
    histories_env_file = "histories_env.jsonl"
    queries_env_file = "queries_env.jsonl"
    histories_prin_file = "histories_prin.jsonl"
    queries_prin_file = "queries_prin.jsonl"
    
    # 检查文件是否存在
    if not os.path.exists(overlong_file):
        print(f"错误: {overlong_file} 文件不存在")
        return
    
    if not os.path.exists(histories_env_file):
        print(f"错误: {histories_env_file} 文件不存在")
        return
    
    if not os.path.exists(queries_env_file):
        print(f"错误: {queries_env_file} 文件不存在")
        return
    
    if not os.path.exists(histories_prin_file):
        print(f"错误: {histories_prin_file} 文件不存在")
        return
    
    if not os.path.exists(queries_prin_file):
        print(f"错误: {queries_prin_file} 文件不存在")
        return
    
    # 加载数据
    print("加载overlong.jsonl...")
    overlong_data = load_jsonl_file(overlong_file)
    print(f"加载了 {len(overlong_data)} 条overlong记录")
    
    print("加载histories_env.jsonl...")
    histories_env_data = load_jsonl_file(histories_env_file)
    print(f"加载了 {len(histories_env_data)} 条histories_env记录")
    
    print("加载queries_env.jsonl...")
    queries_env_data = load_jsonl_file(queries_env_file)
    print(f"加载了 {len(queries_env_data)} 条queries_env记录")
    
    print("加载histories_prin.jsonl...")
    histories_prin_data = load_jsonl_file(histories_prin_file)
    print(f"加载了 {len(histories_prin_data)} 条histories_prin记录")
    
    print("加载queries_prin.jsonl...")
    queries_prin_data = load_jsonl_file(queries_prin_file)
    print(f"加载了 {len(queries_prin_data)} 条queries_prin记录")
    
    # 提取需要删除的查询
    print("提取需要删除的查询...")
    queries_to_delete = extract_queries_from_overlong(overlong_data)
    print(f"找到 {len(queries_to_delete)} 个需要删除的查询")
    
    # 清理所有文件
    print("清理histories_env.jsonl...")
    cleaned_histories_env, deleted_histories_env = clean_histories_file(histories_env_data, queries_to_delete)
    
    print("清理queries_env.jsonl...")
    cleaned_queries_env, deleted_queries_env = clean_queries_file(queries_env_data, queries_to_delete)
    
    print("清理histories_prin.jsonl...")
    cleaned_histories_prin, deleted_histories_prin = clean_histories_file(histories_prin_data, queries_to_delete)
    
    print("清理queries_prin.jsonl...")
    cleaned_queries_prin, deleted_queries_prin = clean_queries_file(queries_prin_data, queries_to_delete)
    
    # 保存清理后的数据
    print("保存清理后的数据...")
    save_jsonl_file(histories_env_file, cleaned_histories_env)
    save_jsonl_file(queries_env_file, cleaned_queries_env)
    save_jsonl_file(histories_prin_file, cleaned_histories_prin)
    save_jsonl_file(queries_prin_file, cleaned_queries_prin)
    
    # 输出统计信息
    print("\n清理完成!")
    print(f"从histories_env.jsonl中删除了 {deleted_histories_env} 条记录")
    print(f"从queries_env.jsonl中删除了 {deleted_queries_env} 条记录")
    print(f"从histories_prin.jsonl中删除了 {deleted_histories_prin} 条记录")
    print(f"从queries_prin.jsonl中删除了 {deleted_queries_prin} 条记录")
    print(f"\n剩余记录数:")
    print(f"histories_env.jsonl: {len(cleaned_histories_env)} 条记录")
    print(f"queries_env.jsonl: {len(cleaned_queries_env)} 条记录")
    print(f"histories_prin.jsonl: {len(cleaned_histories_prin)} 条记录")
    print(f"queries_prin.jsonl: {len(cleaned_queries_prin)} 条记录")

if __name__ == "__main__":
    main()
