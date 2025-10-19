#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据检查脚本：检查 env_data_train_final.jsonl 和 env_data_test_final.jsonl 的合法性
"""

import json
import sys
import os
from pathlib import Path
import statistics
# 添加 Utils 路径
sys.path.append('Utils')
from Utils.utils import is_valid_security

def load_env_info():
    """加载环境信息，合并训练集和测试集数据"""
    try:
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建 Environment 目录的路径
        env_dir = os.path.join(os.path.dirname(script_dir), 'Environment')
        
        # 加载训练集和测试集数据
        train_file = os.path.join(env_dir, 'env_info_train.json')
        test_file = os.path.join(env_dir, 'env_info_test.json')
        
        env_info = {}
        
        # 加载训练集数据
        if os.path.exists(train_file):
            with open(train_file, 'r', encoding='utf-8') as f:
                train_data = json.load(f)
                print(f"  加载训练集数据: {train_file}")
                for category, observations in train_data.items():
                    if category not in env_info:
                        env_info[category] = []
                    env_info[category].extend(observations)
        else:
            print(f"  警告：训练集文件不存在: {train_file}")
        
        # 加载测试集数据
        if os.path.exists(test_file):
            with open(test_file, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
                print(f"  加载测试集数据: {test_file}")
                for category, observations in test_data.items():
                    if category not in env_info:
                        env_info[category] = []
                    env_info[category].extend(observations)
        else:
            print(f"  警告：测试集文件不存在: {test_file}")
        
        return env_info
    except Exception as e:
        print(f"错误：无法加载环境信息: {e}")
        return None

# 风险类型列表
RISK_TYPES = [
    "Safe",
    "Sensitive Data Exfiltration",
    "Covert Channel Attack",
    "Malicious Code Execution",
    "Privilege Escalation",
    "Persistence via Backdoor Implantation",
    "Cache or Local State Pollution",
    "Delayed or Timed Trigger Attacks",
    "Denial-of-Service",
    "Log Explosion Attacks",
]

def is_valid_response(resp_list):
    EXPECTED_ROLES = ["system", "user", "assistant", "user"]
    """Return True if resp_list matches the required structure."""
    if not isinstance(resp_list, list) or len(resp_list) < 4:
        return False
    for elem, role in zip(resp_list[:4], EXPECTED_ROLES):
        if not isinstance(elem, dict) or elem.get("role") != role:
            return False
    return True


def ignore_risk(sec: list) -> bool:
    """
    检查是否应该忽略该风险
    合法格式: [ "safe", "safe", ..., <RiskType> ]
    其中 <RiskType> 必须出现在 RISK_TYPES 中，且列表至少长度 1。
    """
    if not sec or len(sec) == 0:
        return True
    
    # 其余元素只能是 "safe"（忽略大小写）
    prefix = sec[:-1]
    return not all(x.lower() == "safe" for x in prefix)

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

def check_security_type_environment_match(history, security_type, env_info):
    """
    检查 security_type 和 role 为 user 的 turn 的 Environment_status 是否匹配
    """
    user_turns = [turn for turn in history if turn.get('role') == 'user']
    
    # 跳过第一个 user turn（初始查询）
    if len(user_turns) <= 1:
        return True, "没有需要检查的 user turns"
    
    # 检查后续的 user turns
    for i, turn in enumerate(user_turns[1:], 1):  # 从第二个 user turn 开始
        content = turn.get('content', '')
        
        if 'Tool result & environment status:' in content:
            tool_result = parse_tool_result(content)
            if tool_result:
                env_status = tool_result.get('Environment_status', '')
                if i-1 < len(security_type) and security_type[i-1] in env_info:
                    if env_status not in env_info[security_type[i-1]]:
                        return False, f"User turn {i+1} 的 Environment_status 与 security_type[{i-1}] 不匹配"
    
    return True, "所有 user turns 的 Environment_status 与 security_type 匹配"

def check_chosen_rejected(sample, security_type):
    """
    检查 chosen 和 rejected 字段的合法性
    """
    errors = []
    
    chosen = sample.get('chosen', '')
    rejected = sample.get('rejected', '')
    
    if not chosen or not rejected:
        errors.append("chosen 或 rejected 字段为空")
        return errors
    
    # 获取最后一个 security_type
    last_security_type = security_type[-1] if security_type else None
    
    if last_security_type == "Safe":
        # 如果最后一个 Security_type 为 "Safe"，那么 chosen 应该是正常回复
        if chosen.startswith("Unsafe MCP Server:"):
            errors.append("最后一个 security_type 为 'Safe' 时，chosen 不应该是拒绝回复")
        
        # rejected 可以是拒绝回复（即报错 Unsafe MCP Server:）
        if not rejected.startswith("Unsafe MCP Server:"):
            errors.append("最后一个 security_type 为 'Safe' 时，rejected 应该是拒绝回复")
    
    else:
        # 如果是其他的 risk，那么 chosen 应该是拒绝回复且报错这个 risk
        if not chosen.startswith("Unsafe MCP Server:"):
            errors.append(f"最后一个 security_type 为 '{last_security_type}' 时，chosen 应该是拒绝回复")
        else:
            # 检查 chosen 中的 Reason 是否与最后一个 security_type 匹配
            try:
                # 解析 Unsafe MCP Server: 后面的 JSON
                json_start = chosen.find("Unsafe MCP Server:") + len("Unsafe MCP Server:")
                chosen_json = json.loads(chosen[json_start:])
                chosen_reason = chosen_json.get('Reason', '')
                
                if chosen_reason != last_security_type:
                    errors.append(f"chosen 中的 Reason '{chosen_reason}' 与最后一个 security_type '{last_security_type}' 不匹配")
            except:
                errors.append("chosen 中的 JSON 格式不正确")
        
        # rejected 可以是正常回复或者拒绝回复但是报错其他类别
        if rejected.startswith("Unsafe MCP Server:"):
            try:
                # 解析 rejected 中的 JSON
                json_start = rejected.find("Unsafe MCP Server:") + len("Unsafe MCP Server:")
                rejected_json = json.loads(rejected[json_start:])
                rejected_reason = rejected_json.get('Reason', '')
                
                # 检查 rejected 的 Reason 是否与最后一个 security_type 不同
                if rejected_reason == last_security_type:
                    errors.append(f"rejected 中的 Reason '{rejected_reason}' 不应该与最后一个 security_type '{last_security_type}' 相同")
            except:
                errors.append("rejected 中的 JSON 格式不正确")
    
    return errors

def check_single_sample(sample, sample_idx, env_info):
    """
    检查单个样本的合法性
    """
    errors = []
    
    # 1. 检查基本结构
    if not isinstance(sample, dict):
        errors.append("样本不是有效的字典格式")
        return errors
    
    # 2. 检查必要字段
    required_fields = ['server_path', 'query', 'history', 'security_type', 'chosen', 'rejected']
    for field in required_fields:
        if field not in sample:
            errors.append(f"缺少必要字段: {field}")
    
    if errors:
        return errors
    
    # 3. 检查 history 的合法性（参考 curate_train_test.py）
    history = sample.get('history', [])
    if not is_valid_response(history):
        errors.append("history 格式不合法")
    
    # 4. 检查 security_type 的合法性（参考 Utils/utils.py）
    security_type = sample.get('security_type', [])
    if not is_valid_security(security_type):
        errors.append("security_type 格式不合法")
    
    # 5. 检查是否应该忽略该风险
    if ignore_risk(security_type):
        errors.append("该样本忽略了风险（ignore_risk 返回 True）")
    
    # 6. 检查 security_type 长度和 history 长度的关系
    # 公式: 2*len(security_type) + 2 = len(history)
    expected_history_len = 2 * len(security_type) + 2
    actual_history_len = len(history)
    if actual_history_len != expected_history_len:
        errors.append(f"history 长度不匹配: 期望 {expected_history_len}, 实际 {actual_history_len}")
    
    # 7. 检查 security_type 和 Environment_status 的匹配
    match_result, match_message = check_security_type_environment_match(history, security_type, env_info)
    if not match_result:
        errors.append(match_message)
    
    # 8. 检查 chosen 和 rejected 字段的合法性
    chosen_rejected_errors = check_chosen_rejected(sample, security_type)
    errors.extend(chosen_rejected_errors)
    
    return errors

def collect_statistics(file_path):
    """
    收集文件中的统计信息
    """
    risk_counts = {}
    risk_observations = {}
    risk_observation_counts = {}  # 新增：统计每个 observation 的出现次数
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        sample = json.loads(line)
                        security_type = sample.get('security_type', [])
                        
                        # 统计每个 risk 类别的出现次数
                        for risk in security_type:
                            risk_counts[risk] = risk_counts.get(risk, 0) + 1
                        
                        # 收集每个 risk 类别的不同 observations
                        history = sample.get('history', [])
                        user_turns = [turn for turn in history if turn.get('role') == 'user']
                        
                        # 跳过第一个 user turn（初始查询）
                        for i, turn in enumerate(user_turns[1:], 1):  # 从第二个 user turn 开始
                            if i-1 < len(security_type):  # 确保索引不越界
                                risk = security_type[i-1]
                                content = turn.get('content', '')
                                
                                if 'Tool result & environment status:' in content:
                                    tool_result = parse_tool_result(content)
                                    if tool_result:
                                        env_status = tool_result.get('Environment_status', '')
                                        if risk not in risk_observations:
                                            risk_observations[risk] = set()
                                        risk_observations[risk].add(env_status)
                                        
                                        # 统计每个 observation 的出现次数
                                        if risk not in risk_observation_counts:
                                            risk_observation_counts[risk] = {}
                                        if env_status not in risk_observation_counts[risk]:
                                            risk_observation_counts[risk][env_status] = 0
                                        risk_observation_counts[risk][env_status] += 1
                        
                    except json.JSONDecodeError:
                        continue
    
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return {}, {}, {}
    
    return risk_counts, risk_observations, risk_observation_counts

def print_statistics(file_path, risk_counts, risk_observations, risk_observation_counts):
    """
    打印统计信息
    """
    print(f"\n📊 {file_path} 统计信息:")
    print("-" * 50)
    
    # 按风险类型排序
    sorted_risks = sorted(risk_counts.keys())
    
    for risk in sorted_risks:
        count = risk_counts[risk]
        unique_obs = len(risk_observations.get(risk, set()))
        print(f"{risk}: {count} 次, {unique_obs} 种不同 observations")
    
    print("-" * 50)
    print(f"总计: {sum(risk_counts.values())} 个样本")
    
    # 统计所有 observation 的出现次数，并输出最大值、最小值、中位数和平均数
    all_observation_counts = []
    for risk, obs_counts in risk_observation_counts.items():
        all_observation_counts.extend(obs_counts.values())
    
    if all_observation_counts:
        max_count = max(all_observation_counts)
        min_count = min(all_observation_counts)
        median_count = statistics.median(all_observation_counts)
        mean_count = statistics.mean(all_observation_counts)
        print(f"Observation 出现次数 - 最大值: {max_count}, 最小值: {min_count}, 中位数: {median_count:.2f}, 平均数: {mean_count:.2f}")
    else:
        print("未找到任何 observation 数据")

def check_observation_overlap(train_observations, test_observations):
    """
    检查训练集和测试集之间的 observations 重叠情况
    """
    print(f"\n🔍 检查训练集和测试集之间的 observations 重叠情况:")
    print("-" * 60)
    
    # 获取所有风险类型
    all_risks = set(train_observations.keys()) | set(test_observations.keys())
    sorted_risks = sorted(all_risks)
    
    total_overlaps = 0
    total_train_obs = 0
    total_test_obs = 0
    
    for risk in sorted_risks:
        train_obs = train_observations.get(risk, set())
        test_obs = test_observations.get(risk, set())
        
        # 计算重叠
        overlap = train_obs & test_obs
        overlap_count = len(overlap)
        
        train_count = len(train_obs)
        test_count = len(test_obs)
        
        total_overlaps += overlap_count
        total_train_obs += train_count
        total_test_obs += test_count
        
        if train_count > 0 or test_count > 0:
            overlap_percentage = (overlap_count / max(train_count, test_count)) * 100 if max(train_count, test_count) > 0 else 0
            print(f"{risk}:")
            print(f"  训练集: {train_count} 种 observations")
            print(f"  测试集: {test_count} 种 observations")
            print(f"  重叠: {overlap_count} 种 ({overlap_percentage:.1f}%)")
            
            if overlap_count > 0:
                print(f"  ⚠️  发现 {overlap_count} 个重叠的 observations")
            else:
                print(f"  ✅ 无重叠")
            print()
    
    # 总体统计
    print("-" * 60)
    print(f"总体统计:")
    print(f"训练集总 observations: {total_train_obs}")
    print(f"测试集总 observations: {total_test_obs}")
    print(f"总重叠数: {total_overlaps}")
    
    if total_overlaps > 0:
        max_obs = max(total_train_obs, total_test_obs)
        overall_overlap_percentage = (total_overlaps / max_obs) * 100 if max_obs > 0 else 0
        print(f"总体重叠率: {overall_overlap_percentage:.1f}%")
        print(f"⚠️  警告: 发现 {total_overlaps} 个重叠的 observations，可能存在数据泄露风险！")
    else:
        print(f"✅ 无重叠，数据分离良好")
    
    print("-" * 60)
    
    return total_overlaps

def check_file(file_path, env_info):
    """
    检查单个文件
    """
    print(f"检查文件: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    errors_count = 0
    total_samples = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        sample = json.loads(line)
                        total_samples += 1
                        
                        errors = check_single_sample(sample, total_samples, env_info)
                        if errors:
                            print(f"❌ 样本 {total_samples} (行 {line_num}) 有错误:")
                            for error in errors:
                                print(f"   - {error}")
                            errors_count += 1
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ 行 {line_num} JSON 解析错误: {e}")
                        errors_count += 1
                        total_samples += 1
    
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return False
    
    print(f"✅ 文件检查完成: {total_samples} 个样本, {errors_count} 个错误")
    return errors_count == 0

def main():
    """
    主函数
    """
    print("=" * 60)
    print("数据合法性检查工具")
    print("=" * 60)
    
    # 加载环境信息
    print("加载环境信息...")
    env_info = load_env_info()
    if env_info is None:
        print("错误：无法加载环境信息，退出")
        return False
    
    # 检查的文件列表
    files_to_check = [
        "env_data_train.jsonl",
        "env_data_test.jsonl"
    ]
    
    all_passed = True
    all_risk_counts = {}
    all_risk_observations = {}
    train_observations = {}
    test_observations = {}
    
    for file_path in files_to_check:
        print(f"\n{'='*40}")
        
        # 收集统计信息
        risk_counts, risk_observations, risk_observation_counts = collect_statistics(file_path)
        
        # 合并到总统计中
        for risk, count in risk_counts.items():
            all_risk_counts[risk] = all_risk_counts.get(risk, 0) + count
        
        for risk, observations in risk_observations.items():
            if risk not in all_risk_observations:
                all_risk_observations[risk] = set()
            all_risk_observations[risk].update(observations)
        
        # 分别保存训练集和测试集的 observations
        if "train" in file_path:
            train_observations = risk_observations
        elif "test" in file_path:
            test_observations = risk_observations
        
        # 打印单个文件的统计信息
        print_statistics(file_path, risk_counts, risk_observations, risk_observation_counts)
        
        # 检查文件
        if not check_file(file_path, env_info):
            all_passed = False
        print(f"{'='*40}")
    
    # 检查 observations 重叠情况
    if train_observations and test_observations:
        overlap_count = check_observation_overlap(train_observations, test_observations)
        if overlap_count > 0:
            all_passed = False  # 如果有重叠，标记为检查失败
    
    # 打印总体统计信息
    print(f"\n{'='*60}")
    print("📊 总体统计信息:")
    print("-" * 50)
    
    # 按风险类型排序
    sorted_risks = sorted(all_risk_counts.keys())
    
    for risk in sorted_risks:
        count = all_risk_counts[risk]
        unique_obs = len(all_risk_observations.get(risk, set()))
        print(f"{risk}: {count} 次, {unique_obs} 种不同 observations")
    
    print("-" * 50)
    print(f"总计: {sum(all_risk_counts.values())} 个样本")
    print(f"{'='*60}")
    
    if all_passed:
        print("🎉 所有文件检查通过！")
    else:
        print("❌ 部分文件检查失败，请查看上述错误信息")
    print(f"{'='*60}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
