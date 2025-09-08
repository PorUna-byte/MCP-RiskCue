#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：测试PairedPreferenceDataLoader的功能
打印出labels, input_ids, text等信息
"""

import os
import sys
import argparse
import torch
from transformers import AutoTokenizer
from EasyAlign.utils.utils import selective_decode
# 添加项目路径到sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from EasyAlign.dataloaders.dataloader import PairedPreferenceDataLoader
from EasyAlign.configs.config import get_args


class TestConfig:
    """测试用的配置类"""
    def __init__(self):
        # 基本参数
        self.seed = 22
        self.dataset = 'MCPenv'
        self.model_name = 'qwen2-5-7b-instruct'
        self.loss_name = 'dpo'
        
        # 模型路径
        self.model_path = '/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen2.5-7B-Instruct'
        self.tokenizer_path = None  # 将使用model_path
        
        # 数据加载参数
        self.max_length = 2548
        self.max_prompt_length = 2048
        self.max_new_tokens = 500
        self.gen_valid_len = 300
        self.len_penalty = 0.01
        
        # 分布式参数（单GPU测试）
        self.global_rank = 0
        self.world_size = 1
        self.local_rank = 0
        
        # 日志文件
        self.log_file = None
        
        # 前缀和后缀
        self.system_prefix = "<|im_start|>system\n"
        self.system_suffix = "<|im_end|>"
        self.human_prefix = "<|im_start|>user\n"
        self.assistant_prefix = "<|im_start|>assistant\n"
        self.human_suffix = "<|im_end|>"
        self.assistant_suffix = "<|im_end|>"
        
        # DPO相关参数
        self.dpo_beta = 0.1
        self.avg_logp = False
        self.all_turn = False
        
        # 其他参数
        self.policy_dtype = 'bfloat16'
        self.reward_dtype = 'bfloat16'
        self.flash_attention = 'flash_attention_2'


def print_batch_info(batch, batch_idx, tokenizer):
    """打印批次信息"""
    print(f"\n{'='*80}")
    print(f"批次 {batch_idx}")
    print(f"{'='*80}")
    
    # 打印批次大小
    batch_size = len(batch['prompt_text'])
    print(f"批次大小: {batch_size}")
    
    # 打印每个样本的信息
    for i in range(batch_size):
        print(f"\n--- 样本 {i+1} ---")
        
        # 打印chosen信息        
        print(f"Chosen Combined Text: {selective_decode(tokenizer, batch['chosen_combined_input_ids'][i].tolist())}")
        print(f"Chosen Combined Input IDs shape: {batch['chosen_combined_input_ids'][i].shape}")
        print(f"Chosen Combined Input IDs: {batch['chosen_combined_input_ids'][i].tolist()}")
        print(f"Chosen Labels shape: {batch['chosen_labels'][i].shape}")
        print(f"Chosen Labels: {batch['chosen_labels'][i].tolist()}")
        
        # 打印rejected信息
        print(f"Rejected Combined Text: {selective_decode(tokenizer, batch['rejected_combined_input_ids'][i].tolist())}")
        print(f"Rejected Combined Input IDs shape: {batch['rejected_combined_input_ids'][i].shape}")
        print(f"Rejected Combined Input IDs: {batch['rejected_combined_input_ids'][i].tolist()}")
        print(f"Rejected Labels shape: {batch['rejected_labels'][i].shape}")
        print(f"Rejected Labels: {batch['rejected_labels'][i].tolist()}")
        
        # 打印其他信息
        print(f"\nTruncation Mode: {batch['truncation_mode'][i]}")
        print(f"Data Label: {batch['data_label'][i]}")


def test_paired_preference_dataloader():
    """测试PairedPreferenceDataLoader"""
    print("开始测试PairedPreferenceDataLoader...")
    
    # 创建配置
    config = TestConfig()
    print(f"配置创建完成: dataset={config.dataset}, model={config.model_name}")
    
    # 加载tokenizer
    print("正在加载tokenizer...")
    tokenizer_path = config.tokenizer_path or config.model_path
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    print(f"Tokenizer加载完成: {tokenizer_path}")
    
    # 创建DataLoader
    print("正在创建PairedPreferenceDataLoader...")
    dataloader = PairedPreferenceDataLoader(
        config=config,
        tokenizer=tokenizer,
        split='train',
        batch_size=2,  # 小批次用于测试
        n_examples=4   # 只测试4个样本
    )
    print(f"DataLoader创建完成，总样本数: {dataloader.num_prompts}")
    
    # 迭代数据
    print("\n开始迭代数据...")
    batch_count = 0
    max_batches = 2  # 最多测试2个批次
    
    try:
        for batch in dataloader:
            batch_count += 1
            print_batch_info(batch, batch_count, tokenizer)
            
            if batch_count >= max_batches:
                print(f"\n已测试 {batch_count} 个批次，停止测试")
                break
                
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n测试完成！总共处理了 {batch_count} 个批次")


if __name__ == "__main__":
    test_paired_preference_dataloader()
