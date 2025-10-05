#!/usr/bin/env python3
"""
数据格式转换脚本
将env_data_train.jsonl和env_data_test.jsonl转换为统一格式
"""

import json
import os


def process_data_file(input_file, output_file):
    """
    处理单个数据文件，转换为统一格式
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    processed_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, 1):
            try:
                # 解析JSON行
                data = json.loads(line.strip())
                
                # 获取必要字段
                history = data.get('history', [])
                chosen = data.get('chosen', '')
                rejected = data.get('rejected', '')
                security_type = data.get('security_type', [])
                
                # 创建metadata，包含除了history、chosen、rejected、security_type之外的所有字段
                metadata = {}
                for key, value in data.items():
                    if key not in ['history', 'chosen', 'rejected', 'security_type']:
                        metadata[key] = value
                
                # 创建新的数据结构
                new_data = {
                    "prompt": history,
                    "chosen": chosen,
                    "rejected": rejected,
                    "security_type": security_type,
                    "metadata": metadata
                }
                
                # 写入输出文件
                outfile.write(json.dumps(new_data, ensure_ascii=False) + '\n')
                processed_count += 1
                
            except json.JSONDecodeError as e:
                print(f"警告: 第{line_num}行JSON解析失败: {e}")
                continue
            except Exception as e:
                print(f"警告: 第{line_num}行处理失败: {e}")
                continue
    
    print(f"处理完成: {input_file} -> {output_file}")
    print(f"成功处理 {processed_count} 条数据")
    return processed_count


def main():
    """主函数"""
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义输入和输出文件路径
    train_input = os.path.join(script_dir, 'env_data_train.jsonl')
    test_input = os.path.join(script_dir, 'env_data_test.jsonl')
    
    # 统一格式输出文件
    train_output = os.path.join(script_dir, 'train.jsonl')
    test_output = os.path.join(script_dir, 'test.jsonl')
    
    print("开始数据格式转换...")
    print(f"输入文件: {train_input}, {test_input}")
    print(f"输出文件: {train_output}, {test_output}")
    print("-" * 50)
    
    # 检查输入文件是否存在
    if not os.path.exists(train_input):
        print(f"错误: 输入文件不存在 - {train_input}")
        return
    
    if not os.path.exists(test_input):
        print(f"错误: 输入文件不存在 - {test_input}")
        return
    
    # 处理训练数据
    print("处理训练数据...")
    train_count = process_data_file(train_input, train_output)
    
    print()
    
    # 处理测试数据
    print("处理测试数据...")
    test_count = process_data_file(test_input, test_output)
    
    print()
    print("=" * 50)
    print("数据转换完成!")
    print(f"训练数据: {train_count} 条")
    print(f"测试数据: {test_count} 条")
    print(f"输出文件: {train_output}, {test_output}")


if __name__ == "__main__":
    main()
