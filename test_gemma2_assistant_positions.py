#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试函数：探究 Gemma2-2B 模型中 _find_assistant_positions 找不到 <|im_start|> 和 <|im_end|> 位置的原因
"""

import torch
from transformers import AutoTokenizer
import json
from typing import List, Tuple, Dict, Any

def test_gemma2_tokenization():
    """测试 Gemma2-2B 的 tokenization 行为"""
    
    # 加载 Gemma2-2B tokenizer
    model_name = "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Gemma-2-2B"
    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 测试字符串 - 使用 Gemma-2-2B 的特殊 token
    test_strings = [
        "<start_of_turn>assistant\nHello, how can I help you?<end_of_turn>",
        "<start_of_turn>assistant\nThis is a test response.<end_of_turn>",
        "<start_of_turn>user\nWhat is the weather?<end_of_turn>\n<start_of_turn>assistant\nI don't have access to weather data.<end_of_turn>",
        "<start_of_turn>system\nYou are a helpful assistant.<end_of_turn>\n<start_of_turn>user\nHello<end_of_turn>\n<start_of_turn>assistant\nHi there!<end_of_turn>"
    ]
    
    print("\n" + "="*80)
    print("TOKENIZATION ANALYSIS")
    print("="*80)
    
    for i, text in enumerate(test_strings):
        print(f"\n--- Test Case {i+1} ---")
        print(f"Original text: {repr(text)}")
        
        # Tokenize the text
        tokens = tokenizer.encode(text)
        print(f"Token IDs: {tokens}")
        print(f"Number of tokens: {len(tokens)}")
        
        # Decode tokens back to text
        decoded = tokenizer.decode(tokens)
        print(f"Decoded text: {repr(decoded)}")
        
        # Check if decoded text matches original
        if decoded == text:
            print("✅ Perfect round-trip tokenization")
        else:
            print("❌ Round-trip tokenization mismatch")
            print(f"Differences:")
            print(f"  Original: {repr(text)}")
            print(f"  Decoded:  {repr(decoded)}")
        
        # Analyze special tokens
        print("\nSpecial token analysis:")
        
        # Check for <start_of_turn> and <end_of_turn>
        start_turn_tokens = tokenizer.encode("<start_of_turn>")
        end_turn_tokens = tokenizer.encode("<end_of_turn>")
        
        # Remove BOS token if present
        if tokenizer.bos_token_id is not None and len(start_turn_tokens) > 0 and start_turn_tokens[0] == tokenizer.bos_token_id:
            start_turn_tokens = start_turn_tokens[1:]
        if tokenizer.bos_token_id is not None and len(end_turn_tokens) > 0 and end_turn_tokens[0] == tokenizer.bos_token_id:
            end_turn_tokens = end_turn_tokens[1:]
        
        print(f"<start_of_turn> tokens (no BOS): {start_turn_tokens}")
        print(f"<end_of_turn> tokens (no BOS): {end_turn_tokens}")
        
        # Check if these tokens exist in the main text
        start_turn_found = any(tokens[j:j+len(start_turn_tokens)] == start_turn_tokens 
                             for j in range(len(tokens) - len(start_turn_tokens) + 1))
        end_turn_found = any(tokens[j:j+len(end_turn_tokens)] == end_turn_tokens 
                           for j in range(len(tokens) - len(end_turn_tokens) + 1))
        
        print(f"<start_of_turn> found in text: {start_turn_found}")
        print(f"<end_of_turn> found in text: {end_turn_found}")
        
        # Try to find positions manually
        if start_turn_found:
            positions = []
            for j in range(len(tokens) - len(start_turn_tokens) + 1):
                if tokens[j:j+len(start_turn_tokens)] == start_turn_tokens:
                    positions.append(j)
            print(f"<start_of_turn> positions: {positions}")
        
        if end_turn_found:
            positions = []
            for j in range(len(tokens) - len(end_turn_tokens) + 1):
                if tokens[j:j+len(end_turn_tokens)] == end_turn_tokens:
                    positions.append(j)
            print(f"<end_of_turn> positions: {positions}")

def test_assistant_prefix_suffix():
    """测试 assistant prefix 和 suffix 的 tokenization"""
    
    model_name = "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Gemma-2-2B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 常见的 assistant prefix 和 suffix - 使用 Gemma-2-2B 格式
    assistant_prefixes = [
        "<start_of_turn>assistant\n",
        "<start_of_turn>assistant",
        "assistant\n",
        "assistant"
    ]
    
    assistant_suffixes = [
        "<end_of_turn>",
        "<end_of_turn>\n",
        "\n<end_of_turn>"
    ]
    
    print("\n" + "="*80)
    print("ASSISTANT PREFIX/SUFFIX ANALYSIS")
    print("="*80)
    
    for prefix in assistant_prefixes:
        print(f"\nPrefix: {repr(prefix)}")
        tokens = tokenizer.encode(prefix)
        print(f"Tokens: {tokens}")
        decoded = tokenizer.decode(tokens)
        print(f"Decoded: {repr(decoded)}")
        print(f"Round-trip match: {decoded == prefix}")
    
    for suffix in assistant_suffixes:
        print(f"\nSuffix: {repr(suffix)}")
        tokens = tokenizer.encode(suffix)
        print(f"Tokens: {tokens}")
        decoded = tokenizer.decode(tokens)
        print(f"Decoded: {repr(decoded)}")
        print(f"Round-trip match: {decoded == suffix}")

def test_special_tokens_behavior():
    """测试特殊 token 的行为"""
    
    model_name = "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Gemma-2-2B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    print("\n" + "="*80)
    print("SPECIAL TOKENS BEHAVIOR ANALYSIS")
    print("="*80)
    
    # 检查 tokenizer 的特殊 token 设置
    print(f"Special tokens map: {tokenizer.special_tokens_map}")
    print(f"Additional special tokens: {tokenizer.additional_special_tokens}")
    print(f"All special tokens: {tokenizer.all_special_tokens}")
    
    # 测试各种特殊 token 组合 - 使用 Gemma-2-2B 格式
    special_combinations = [
        "<start_of_turn>",
        "<end_of_turn>",
        "<start_of_turn>assistant",
        "assistant<end_of_turn>",
        "<start_of_turn>assistant<end_of_turn>",
        "<start_of_turn>assistant\n",
        "\n<end_of_turn>",
        "<start_of_turn>assistant\nHello<end_of_turn>"
    ]
    
    for combo in special_combinations:
        print(f"\nTesting: {repr(combo)}")
        tokens = tokenizer.encode(combo)
        print(f"Tokens: {tokens}")
        decoded = tokenizer.decode(tokens)
        print(f"Decoded: {repr(decoded)}")
        
        # 检查是否有特殊的 token ID
        special_token_ids = []
        for token_id in tokens:
            if token_id >= tokenizer.vocab_size:
                special_token_ids.append(token_id)
        
        if special_token_ids:
            print(f"Special token IDs found: {special_token_ids}")
        else:
            print("No special token IDs found")

def test_tokenizer_consistency():
    """测试 tokenizer 的一致性"""
    
    model_name = "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Gemma-2-2B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    print("\n" + "="*80)
    print("TOKENIZER CONSISTENCY TEST")
    print("="*80)
    
    # 测试相同的字符串多次 tokenize 是否一致
    test_text = "<start_of_turn>assistant\nHello world<end_of_turn>"
    
    print(f"Test text: {repr(test_text)}")
    
    # 多次 tokenize
    results = []
    for i in range(5):
        tokens = tokenizer.encode(test_text)
        results.append(tokens)
        print(f"Run {i+1}: {tokens}")
    
    # 检查一致性
    all_same = all(result == results[0] for result in results)
    print(f"All results identical: {all_same}")
    
    # 测试 decode-encode 循环
    print("\nDecode-encode cycle test:")
    original_tokens = tokenizer.encode(test_text)
    decoded_text = tokenizer.decode(original_tokens)
    reencoded_tokens = tokenizer.encode(decoded_text)
    
    print(f"Original tokens: {original_tokens}")
    print(f"Decoded text: {repr(decoded_text)}")
    print(f"Re-encoded tokens: {reencoded_tokens}")
    print(f"Tokens match after cycle: {original_tokens == reencoded_tokens}")

def simulate_find_assistant_positions():
    """模拟 _find_assistant_positions 函数的行为"""
    
    model_name = "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Gemma-2-2B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    print("\n" + "="*80)
    print("SIMULATING _find_assistant_positions")
    print("="*80)
    
    # 模拟配置 - 使用 Gemma-2-2B 格式
    class MockConfig:
        assistant_prefix = "<start_of_turn>assistant\n"
        assistant_suffix = "<end_of_turn>"
    
    config = MockConfig()
    
    # 测试文本
    test_text = "<start_of_turn>user\nWhat is the weather?<end_of_turn>\n<start_of_turn>assistant\nI don't have weather data.<end_of_turn>"
    
    print(f"Test text: {repr(test_text)}")
    print(f"Assistant prefix: {repr(config.assistant_prefix)}")
    print(f"Assistant suffix: {repr(config.assistant_suffix)}")
    
    # 模拟 _find_assistant_positions 逻辑
    combined_tokens = tokenizer.encode(test_text)
    prefix_tokens = tokenizer.encode(config.assistant_prefix)
    suffix_tokens = tokenizer.encode(config.assistant_suffix)
    
    # Remove BOS token if present
    if tokenizer.bos_token_id is not None and len(prefix_tokens) > 0 and prefix_tokens[0] == tokenizer.bos_token_id:
        prefix_tokens = prefix_tokens[1:]
    if tokenizer.bos_token_id is not None and len(suffix_tokens) > 0 and suffix_tokens[0] == tokenizer.bos_token_id:
        suffix_tokens = suffix_tokens[1:]
    
    print(f"\nCombined tokens: {combined_tokens}")
    print(f"Prefix tokens (no BOS): {prefix_tokens}")
    print(f"Suffix tokens (no BOS): {suffix_tokens}")
    
    assistant_positions = []
    i = 0
    
    print(f"\nSearching for assistant positions...")
    
    while i < len(combined_tokens):
        print(f"Checking position {i}")
        
        # 尝试精确匹配
        if combined_tokens[i:i+len(prefix_tokens)] == prefix_tokens:
            print(f"  Found exact prefix match at position {i}")
            start_pos = i
            prefix_found = True
        else:
            # 尝试去掉尾随空格的匹配
            prefix_without_space = config.assistant_prefix.rstrip()
            prefix_tokens_no_space = tokenizer.encode(prefix_without_space)
            if combined_tokens[i:i+len(prefix_tokens_no_space)] == prefix_tokens_no_space:
                print(f"  Found prefix match (no space) at position {i}")
                start_pos = i
                prefix_found = True
            else:
                prefix_found = False
        
        if prefix_found:
            print(f"  Looking for suffix starting from position {start_pos}")
            j = start_pos
            suffix_found = False
            
            while j < len(combined_tokens):
                if combined_tokens[j:j+len(suffix_tokens)] == suffix_tokens:
                    end_pos = j + len(suffix_tokens)
                    assistant_positions.append((start_pos, end_pos))
                    print(f"  Found complete assistant response: ({start_pos}, {end_pos})")
                    i = j + len(suffix_tokens)
                    suffix_found = True
                    break
                j += 1
            
            if not suffix_found:
                print(f"  No suffix found, looking for next prefix...")
                # 简化版本：直接跳到下一个位置
                i += 1
        else:
            i += 1
    
    print(f"\nFinal assistant positions: {assistant_positions}")
    
    # 验证结果
    if assistant_positions:
        for start, end in assistant_positions:
            assistant_tokens = combined_tokens[start:end]
            assistant_text = tokenizer.decode(assistant_tokens)
            print(f"Assistant text at ({start}, {end}): {repr(assistant_text)}")
    else:
        print("❌ No assistant positions found!")

def main():
    """主函数"""
    print("Gemma2-2B Assistant Positions Debugging Tool")
    print("=" * 80)
    
    try:
        test_gemma2_tokenization()
        test_assistant_prefix_suffix()
        test_special_tokens_behavior()
        test_tokenizer_consistency()
        simulate_find_assistant_positions()
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
