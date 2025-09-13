#!/usr/bin/env python3
"""
脚本用于平衡 Log Explosion Attacks 类别的数据
从 Safe 类别中选取一些数据，将最后一个 risk 类别改为 Log Explosion Attacks
"""

import json
import random
import sys
import os
sys.path.append('Environment')

# 导入 env_info
from env_info import env_info

def load_jsonl(file_path):
    """加载 JSONL 文件"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def save_jsonl(data, file_path):
    """保存 JSONL 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def parse_tool_result(content):
    """
    解析 "Tool result & environment status:" 后面的 JSON 字典
    """
    if "Tool result & environment status:" not in content:
        return None
    
    try:
        # 找到 JSON 开始位置
        json_start = content.find("Tool result & environment status:") + len("Tool result & environment status:")
        json_start = content.find("{", json_start)
        if json_start == -1:
            return None
        
        # 找到 JSON 结束位置
        brace_count = 0
        json_end = json_start
        for i, char in enumerate(content[json_start:], json_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break
        
        json_str = content[json_start:json_end]
        return json.loads(json_str)
    except:
        return None

def find_safe_samples(data, target_count):
    """
    找到 security_type 列表中最后一个元素为 "Safe" 的样本
    """
    safe_samples = []
    
    for item in data:
        security_type = item.get('security_type', [])
        
        # 检查 security_type 列表的最后一个元素是否为 "Safe"
        if security_type and security_type[-1] == "Safe":
            safe_samples.append(item)
            
        if len(safe_samples) >= target_count:
            break
    
    return safe_samples

def extract_server_and_tool_from_assistant(sample):
    """
    从 assistant role 中提取 ServerName 和 ToolName
    """
    history = sample.get('history', [])
    
    # 找到最后一个 user role 的前一个 assistant role
    user_indices = [i for i, turn in enumerate(history) if turn.get('role') == 'user']
    if not user_indices or len(user_indices) <= 1:
        return None, None
    
    last_user_idx = user_indices[-1]
    # 找到最后一个 user role 之前的最后一个 assistant role
    assistant_idx = None
    for i in range(last_user_idx - 1, -1, -1):
        if history[i].get('role') == 'assistant':
            assistant_idx = i
            break
    
    if assistant_idx is None:
        return None, None
    
    assistant_content = history[assistant_idx].get('content', '')
    
    # 解析 JSON 格式的 tool call
    try:
        if 'MCP tool-call message:' in assistant_content:
            json_start = assistant_content.find('MCP tool-call message:') + len('MCP tool-call message:')
            json_start = assistant_content.find('{', json_start)
            if json_start == -1:
                return None, None
            
            # 找到 JSON 结束位置
            brace_count = 0
            json_end = json_start
            for i, char in enumerate(assistant_content[json_start:], json_start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            json_str = assistant_content[json_start:json_end]
            tool_call = json.loads(json_str)
            
            server_name = tool_call.get('server', '')
            tool_name = tool_call.get('tool', '')
            
            return server_name, tool_name
    except:
        pass
    
    return None, None

def convert_safe_to_log_explosion(sample, log_explosion_observations):
    """
    将 Safe 样本转换为 Log Explosion Attacks 样本
    """
    # 深拷贝样本
    new_sample = json.loads(json.dumps(sample))
    
    # 修改 security_type 列表的最后一个元素
    security_type = new_sample.get('security_type', [])
    if security_type and security_type[-1] == "Safe":
        security_type[-1] = "Log Explosion Attacks"
        new_sample['security_type'] = security_type
    
    # 修改 Chosen 和 Rejected
    if 'chosen' in new_sample:
        # 将原来的 chosen 移到 rejected
        new_sample['rejected'] = new_sample['chosen']
        
        # 从 assistant role 中提取 ServerName 和 ToolName
        server_name, tool_name = extract_server_and_tool_from_assistant(sample)
        
        if server_name and tool_name:
            # 创建新的 chosen，格式为 "Unsafe MCP Server:{...}"
            new_chosen = f"Unsafe MCP Server:{json.dumps({'ServerName': server_name, 'ToolName': tool_name, 'Reason': 'Log Explosion Attacks'}, ensure_ascii=False)}"
            new_sample['chosen'] = new_chosen
        else:
            # 如果无法提取，使用默认值
            new_chosen = f"Unsafe MCP Server:{json.dumps({'ServerName': 'UnknownServer', 'ToolName': 'unknown_tool', 'Reason': 'Log Explosion Attacks'}, ensure_ascii=False)}"
            new_sample['chosen'] = new_chosen
    
    # 修改 history[-1]['content'] 中的 Environment_status
    new_history = new_sample.get('history', [])
    if new_history:
        last_content = new_history[-1].get('content', '')
        
        # 解析 "Tool result & environment status:" 后面的 JSON
        tool_result_data = parse_tool_result(last_content)
        if tool_result_data and log_explosion_observations:
            # 随机选择一个 Log Explosion Attacks 的 observation
            random_observation = random.choice(log_explosion_observations)
            
            # 更新 Environment_status
            tool_result_data['Environment_status'] = random_observation
            
            # 重新构建 content
            # 找到 JSON 开始和结束位置
            json_start = last_content.find("Tool result & environment status:") + len("Tool result & environment status:")
            json_start = last_content.find("{", json_start)
            
            if json_start != -1:
                # 找到 JSON 结束位置
                brace_count = 0
                json_end = json_start
                for i, char in enumerate(last_content[json_start:], json_start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break
                
                # 替换 JSON 部分
                new_json_str = json.dumps(tool_result_data, ensure_ascii=False)
                new_content = last_content[:json_start] + new_json_str + last_content[json_end:]
                new_history[-1]['content'] = new_content
    
    return new_sample

def balance_log_explosion_attacks(train_file, test_file, output_train_file, output_test_file):
    """
    平衡 Log Explosion Attacks 类别的数据
    """
    print("开始平衡 Log Explosion Attacks 数据...")
    
    # 加载数据
    print("加载训练集...")
    train_data = load_jsonl(train_file)
    print(f"训练集样本数: {len(train_data)}")
    
    print("加载测试集...")
    test_data = load_jsonl(test_file)
    print(f"测试集样本数: {len(test_data)}")
    
    # 获取 Log Explosion Attacks 的 observations
    all_log_explosion_observations = env_info.get('Log Explosion Attacks', [])
    print(f"Log Explosion Attacks 可用 observations: {len(all_log_explosion_observations)}")
    
    # 分割 observations：训练集使用前90%，测试集使用后10%
    split_point = int(len(all_log_explosion_observations) * 0.9)
    train_observations = all_log_explosion_observations[:split_point]
    test_observations = all_log_explosion_observations[split_point:]
    
    print(f"训练集使用 observations: {len(train_observations)} 个 (前90%)")
    print(f"测试集使用 observations: {len(test_observations)} 个 (后10%)")
    
    # 统计当前 Log Explosion Attacks 的数量
    def count_log_explosion(data):
        count = 0
        for item in data:
            security_type = item.get('security_type', [])
            if security_type and security_type[-1] == "Log Explosion Attacks":
                count += 1
        return count
    
    train_log_explosion_count = count_log_explosion(train_data)
    test_log_explosion_count = count_log_explosion(test_data)
    
    print(f"当前训练集 Log Explosion Attacks 数量: {train_log_explosion_count}")
    print(f"当前测试集 Log Explosion Attacks 数量: {test_log_explosion_count}")
    
    # 设置需要转换的数量
    train_need = 400  # 训练集转换 550 个
    test_need = 60    # 测试集转换 60 个
    
    print(f"训练集需要转换 {train_need} 个样本")
    print(f"测试集需要转换 {test_need} 个样本")
    
    # 处理训练集
    if train_need > 0:
        print(f"\n处理训练集，寻找 {train_need} 个 Safe 样本...")
        safe_samples = find_safe_samples(train_data, train_need)
        print(f"找到 {len(safe_samples)} 个 Safe 样本")
        
        # 随机选择需要转换的样本
        selected_samples = random.sample(safe_samples, min(train_need, len(safe_samples)))
        
        # 转换样本
        converted_samples = []
        for sample in selected_samples:
            converted = convert_safe_to_log_explosion(sample, train_observations)
            converted_samples.append(converted)
        
        # 从原数据中移除被转换的样本，添加转换后的样本
        sample_ids = {id(s) for s in selected_samples}
        remaining_data = [item for item in train_data if id(item) not in sample_ids]
        train_data = remaining_data + converted_samples
        
        print(f"训练集转换完成，新增 {len(converted_samples)} 个 Log Explosion Attacks 样本")
    
    # 处理测试集
    if test_need > 0:
        print(f"\n处理测试集，寻找 {test_need} 个 Safe 样本...")
        safe_samples = find_safe_samples(test_data, test_need)
        print(f"找到 {len(safe_samples)} 个 Safe 样本")
        
        # 随机选择需要转换的样本
        selected_samples = random.sample(safe_samples, min(test_need, len(safe_samples)))
        
        # 转换样本
        converted_samples = []
        for sample in selected_samples:
            converted = convert_safe_to_log_explosion(sample, test_observations)
            converted_samples.append(converted)
        
        # 从原数据中移除被转换的样本，添加转换后的样本
        sample_ids = {id(s) for s in selected_samples}
        remaining_data = [item for item in test_data if id(item) not in sample_ids]
        test_data = remaining_data + converted_samples
        
        print(f"测试集转换完成，新增 {len(converted_samples)} 个 Log Explosion Attacks 样本")
    
    # 保存结果
    print(f"\n保存结果...")
    save_jsonl(train_data, output_train_file)
    save_jsonl(test_data, output_test_file)
    
    print(f"✅ 训练集已保存到: {output_train_file}")
    print(f"✅ 测试集已保存到: {output_test_file}")
    
    # 验证结果
    print(f"\n验证结果...")
    final_train_count = count_log_explosion(train_data)
    final_test_count = count_log_explosion(test_data)
    
    print(f"最终训练集 Log Explosion Attacks 数量: {final_train_count}")
    print(f"最终测试集 Log Explosion Attacks 数量: {final_test_count}")

def main():
    print("=" * 60)
    print("Log Explosion Attacks 数据平衡工具")
    print("=" * 60)
    
    # 文件路径
    train_file = "Data/env_data_train_filter.jsonl"
    test_file = "Data/env_data_test_filter.jsonl"
    output_train_file = "Data/env_data_train_balanced.jsonl"
    output_test_file = "Data/env_data_test_balanced.jsonl"
    
    # 检查输入文件是否存在
    if not os.path.exists(train_file):
        print(f"❌ 训练集文件不存在: {train_file}")
        return
    
    if not os.path.exists(test_file):
        print(f"❌ 测试集文件不存在: {test_file}")
        return
    
    # 执行平衡
    balance_log_explosion_attacks(train_file, test_file, output_train_file, output_test_file)
    
    print("\n" + "=" * 60)
    print("数据平衡完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
