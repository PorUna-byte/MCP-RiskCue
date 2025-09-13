#!/usr/bin/env python3
"""
数据转换脚本：处理 env_data_train.jsonl 和 env_data_test.jsonl
1. 读取 history 中 role 为 user 的 turns（除了第一个）
2. 根据 security_type 替换 Environment_status 的值
3. 过滤数据，确保每个 server_path 出现次数不超过3次
"""

import json
import random
import sys
import os
from collections import defaultdict, Counter

# 添加 Environment 目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Environment'))

def load_env_info():
    """加载 env_info 字典"""
    try:
        from env_info import env_info
        return env_info
    except ImportError as e:
        print(f"错误：无法导入 env_info: {e}")
        return None

def prepare_observation_pools(env_info, is_train=True):
    """
    准备观察结果池，训练集使用前90%，测试集使用后10%
    
    Args:
        env_info (dict): 环境信息字典
        is_train (bool): 是否为训练集
        
    Returns:
        dict: 每个类别对应的观察结果池
    """
    observation_pools = {}
    
    for category, observations in env_info.items():
        total_count = len(observations)
        
        if is_train:
            # 训练集使用前90%
            end_idx = int(total_count * 0.9)
            pool = observations[:end_idx]
            print(f"  {category}: 训练集使用前 {end_idx}/{total_count} 个观察结果")
        else:
            # 测试集使用后10%
            start_idx = int(total_count * 0.9)
            pool = observations[start_idx:]
            print(f"  {category}: 测试集使用后 {len(pool)}/{total_count} 个观察结果")
        
        observation_pools[category] = pool
    
    return observation_pools

class UniformSampler:
    """均匀采样器，确保每个observation被采样的次数尽可能均匀"""
    
    def __init__(self, observations):
        self.observations = observations
        self.usage_count = Counter()
        self.total_observations = len(observations)
        self.sample_index = 0  # 当前采样索引
        
    def sample(self):
        """均匀采样一个observation"""
        if not self.observations:
            return None
            
        # 使用轮询方式确保均匀分布
        selected = self.observations[self.sample_index % self.total_observations]
        self.sample_index += 1
        self.usage_count[selected] += 1
        
        return selected
    
    def get_stats(self):
        """获取采样统计信息"""
        if not self.usage_count:
            return "未采样"
        
        counts = list(self.usage_count.values())
        return f"总采样次数: {sum(counts)}, 最小: {min(counts)}, 最大: {max(counts)}, 标准差: {sum((x - sum(counts)/len(counts))**2 for x in counts)**0.5 / len(counts):.2f}"

def parse_tool_result(content):
    """
    解析 "Tool result & environment status:" 后面的 JSON 字典
    
    Args:
        content (str): 包含工具结果的字符串
        
    Returns:
        dict or None: 解析出的字典，如果解析失败返回 None
    """
    try:
        # 查找 "Tool result & environment status:" 后面的内容
        prefix = "Tool result & environment status:\n"
        if prefix in content:
            json_str = content.split(prefix, 1)[1].strip()
            return json.loads(json_str)
        return None
    except (json.JSONDecodeError, IndexError) as e:
        print(f"解析工具结果失败: {e}")
        return None

def process_data_entry(entry, samplers):
    """
    处理单条数据条目
    
    Args:
        entry (dict): 数据条目
        samplers (dict): 每个类别对应的均匀采样器
        
    Returns:
        dict: 处理后的数据条目
    """
    # 创建条目的副本
    processed_entry = entry.copy()
    
    # 获取 security_type
    security_types = entry.get('security_type', [])
    
    # 处理 history 中的 user turns（除了第一个）
    history = entry.get('history', [])
    user_turns = [turn for turn in history if turn.get('role') == 'user']
    
    # 跳过第一个 user turn，处理后面的 turns
    tool_result_turns = user_turns[1:] if len(user_turns) > 1 else []
    
    # 为每个工具结果 turn 分配一个 security_type
    for i, turn in enumerate(tool_result_turns):
        if i < len(security_types):
            security_type = security_types[i]
            
            # 解析工具结果
            tool_result_dict = parse_tool_result(turn['content'])
            if tool_result_dict and 'Environment_status' in tool_result_dict:
                # 从对应的 security_type 中均匀采样一个 observation
                if security_type in samplers:
                    sampler = samplers[security_type]
                    new_environment_status = sampler.sample()
                    if new_environment_status:
                        tool_result_dict['Environment_status'] = new_environment_status
                        
                        # 更新 turn 的 content
                        prefix = "Tool result & environment status:\n"
                        if prefix in turn['content']:
                            json_str = json.dumps(tool_result_dict, indent=2)
                            turn['content'] = prefix + json_str
    
    return processed_entry

def filter_data_by_server_path(data, max_count=3):
    """
    过滤数据，确保每个 server_path 出现次数不超过 max_count
    
    Args:
        data (list): 数据列表
        max_count (int): 每个 server_path 的最大出现次数
        
    Returns:
        list: 过滤后的数据列表
    """
    server_path_counts = defaultdict(int)
    filtered_data = []
    
    for entry in data:
        server_path = entry.get('server_path', '')
        if server_path_counts[server_path] < max_count:
            filtered_data.append(entry)
            server_path_counts[server_path] += 1
    
    return filtered_data

def process_jsonl_file(input_file, output_file, env_info, is_train=True):
    """
    处理 JSONL 文件
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
        env_info (dict): 环境信息字典
        is_train (bool): 是否为训练集
    """
    print(f"处理文件: {input_file}")
    print(f"  数据类型: {'训练集' if is_train else '测试集'}")
    
    # 准备观察结果池
    print("  准备观察结果池...")
    observation_pools = prepare_observation_pools(env_info, is_train)
    
    # 创建均匀采样器
    samplers = {}
    for category, observations in observation_pools.items():
        samplers[category] = UniformSampler(observations)
    
    # 读取数据
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line.strip())
                data.append(entry)
            except json.JSONDecodeError as e:
                print(f"警告：第 {line_num} 行 JSON 解析失败: {e}")
                continue
    
    print(f"  读取了 {len(data)} 条数据")
    
    # 处理数据
    processed_data = []
    for i, entry in enumerate(data):
        try:
            processed_entry = process_data_entry(entry, samplers)
            processed_data.append(processed_entry)
        except Exception as e:
            print(f"警告：处理第 {i+1} 条数据时出错: {e}")
            continue
    
    print(f"  处理了 {len(processed_data)} 条数据")
    
    # 过滤数据
    filtered_data = filter_data_by_server_path(processed_data, max_count=30)
    print(f"  过滤后剩余 {len(filtered_data)} 条数据")
    
    # 统计 server_path 分布
    server_path_counts = defaultdict(int)
    for entry in filtered_data:
        server_path = entry.get('server_path', '')
        server_path_counts[server_path] += 1
    
    print(f"  server_path 分布:")
    for server_path, count in sorted(server_path_counts.items()):
        print(f"    {server_path}: {count} 次")
    
    # 显示采样统计信息
    print(f"  采样统计信息:")
    for category, sampler in samplers.items():
        stats = sampler.get_stats()
        print(f"    {category}: {stats}")
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in filtered_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"  已保存到: {output_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("数据转换脚本")
    print("=" * 60)
    
    # 加载 env_info
    print("1. 加载 env_info...")
    env_info = load_env_info()
    if env_info is None:
        print("错误：无法加载 env_info，退出")
        return
    
    print(f"   ✓ 成功加载 env_info，包含 {len(env_info)} 个类别")
    
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 处理训练数据
    print("\n2. 处理训练数据...")
    train_input = os.path.join(script_dir, 'env_data_train.jsonl')
    train_output = os.path.join(script_dir, 'env_data_train_filter.jsonl')
    
    if os.path.exists(train_input):
        process_jsonl_file(train_input, train_output, env_info, is_train=True)
    else:
        print(f"  警告：文件不存在: {train_input}")
    
    # 处理测试数据
    print("\n3. 处理测试数据...")
    test_input = os.path.join(script_dir, 'env_data_test.jsonl')
    test_output = os.path.join(script_dir, 'env_data_test_filter.jsonl')
    
    if os.path.exists(test_input):
        process_jsonl_file(test_input, test_output, env_info, is_train=False)
    else:
        print(f"  警告：文件不存在: {test_input}")
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
