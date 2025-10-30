#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline for automated model evaluation across different LLM models.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
import argparse
from dotenv import load_dotenv

# 设置环境变量以避免 FX 符号追踪问题
os.environ["TORCH_COMPILE_DEBUG"] = "0"
os.environ["TORCH_LOGS"] = "-dynamo"
os.environ["TORCH_DYNAMO_DISABLE"] = "1"  # 完全禁用 dynamo
os.environ["TORCH_COMPILE_DISABLE"] = "1"  # 禁用 torch.compile
os.environ["TRANSFORMERS_VERBOSITY"] = "error"  # 减少 transformers 日志

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent   

MODEL_INFO = {
    #API models
    "claude-3-7-sonnet-20250219": {
        "local": False,
    },
    "doubao-1-5-pro-32k-250115": {
        "local": False,
    },
    "gemini-2.5-pro": {
        "local": False,
    },
    "glm-4.5v": {
        "local": False,
    },
    "grok-4": {
        "local": False,
    },
    "gpt-4o": {
        "local": False,
    },
    "gpt-5-2025-08-07": {
        "local": False,
    },
    "deepseek-r1": {
        "local": False,
    },
    "kimi-k2-0711-preview": {
        "local": False,
    },
    "o3-2025-04-16": {
        "local": False,
    },
    # 本地模型
    "Qwen3-4B-Instruct": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Instruct-2507",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Instruct-2507",
    },
    "sft_Qwen3-4B-Instruct": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/sft_Qwen3-4B-Instruct-2507",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Instruct-2507",
    },
    "grpo_Qwen3-4B-Instruct": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/grpo_Qwen3-4B-Instruct-2507",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Instruct-2507",
    },
    
    "Llama3.1-8B-Instruct": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-3.1-8B-Instruct",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-3.1-8B-Instruct",
    },
    "sft_Llama3.1-8B-Instruct": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/sft_Llama-3.1-8B-Instruct",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-3.1-8B-Instruct",
    },
    "grpo_Llama3.1-8B-Instruct": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/grpo_Llama-3.1-8B-Instruct",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-3.1-8B-Instruct",
    },  
    
    "DeepSeek-R1-0528-Qwen3-8B": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/DeepSeek-R1-0528-Qwen3-8B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/DeepSeek-R1-0528-Qwen3-8B",
    },
    "sft_DeepSeek-R1-0528-Qwen3-8B": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/sft_DeepSeek-R1-0528-Qwen3-8B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/DeepSeek-R1-0528-Qwen3-8B",
    },
    "grpo_DeepSeek-R1-0528-Qwen3-8B": {
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/grpo_DeepSeek-R1-0528-Qwen3-8B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/DeepSeek-R1-0528-Qwen3-8B",
    },
    "Qwen3-4B-Thinking-2507":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Thinking-2507",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Thinking-2507",
    },
    "sft_Qwen3-4B-Thinking-2507":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/sft_Qwen3-4B-Thinking-2507",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Thinking-2507",
    },
    "grpo_Qwen3-4B-Thinking-2507":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/grpo_Qwen3-4B-Thinking-2507",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B-Thinking-2507",
    },
    
    "Qwen3Guard-Gen-4B":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3Guard-Gen-4B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B",
    },
    "sft_Qwen3Guard-Gen-4B":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/sft_Qwen3Guard-Gen-4B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B",
    },
    "grpo_Qwen3Guard-Gen-4B":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/grpo_Qwen3Guard-Gen-4B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Qwen3-4B",
    },
    "Llama-Guard-3-8B":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-Guard-3-8B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-3.1-8B-Instruct",
    },
    "sft_Llama-Guard-3-8B":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/sft_Llama-Guard-3-8B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-3.1-8B-Instruct",
    },
    "grpo_Llama-Guard-3-8B":{
        "local": True,
        "model_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/grpo_Llama-Guard-3-8B",
        "tokenizer_path": "/mnt/data-alpha-sg-02/team-agent/s00513066/checkpoints_mcp/Llama-3.1-8B-Instruct",
    },
}
# 默认要处理的模型列表（可以从MODEL_INFO中选择）
DEFAULT_MODELS = [
    "claude-3-7-sonnet-20250219",  
    "doubao-1-5-pro-32k-250115",
    "gemini-2.5-pro", 
    "glm-4.5v", 
    "grok-4", 
    "gpt-4o",
    "gpt-5-2025-08-07",
    "deepseek-r1",
    "kimi-k2-0711-preview",
    "o3-2025-04-16",
]

# 数据文件路径
DATA_FILES = {
    "prin": PROJECT_ROOT / "Data" / "prin_data_test.jsonl",
    "env": PROJECT_ROOT / "Data" / "env_data_test.jsonl"
}

# 系统提示文件路径
SYSTEM_PROMPTS = {
    "prin": PROJECT_ROOT / "Prompts" / "sys_prompt_prin.txt",
    "env": PROJECT_ROOT / "Prompts" / "sys_prompt_env.txt"
}

# 输出目录结构
OUTPUT_DIR = Path(__file__).resolve().parent
HISTORY_DIR = OUTPUT_DIR / "history" / "remote"
EVALUATION_DIR = OUTPUT_DIR / "evaluation" / "remote"

# 创建必要的目录
HISTORY_DIR.mkdir(exist_ok=True)
EVALUATION_DIR.mkdir(exist_ok=True)

class ProgressMonitor:
    """简化的进度监控器"""
    
    def __init__(self, total_models: int):
        self.total_models = total_models
        self.current_model = 0
        self.start_time = time.time()
        
    def update_model(self, model_name: str):
        """更新当前处理的模型"""
        self.current_model += 1
        total_elapsed = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print(f"🚀 Processing model {self.current_model}/{self.total_models}: {model_name}")
        print(f"⏱️  Total time: {total_elapsed:.1f}s")
        
        if self.current_model > 0:
            avg_time = total_elapsed / self.current_model
            remaining = self.total_models - self.current_model
            estimated = remaining * avg_time
            print(f"📈 Estimated remaining: {estimated/3600:.1f}h")
        
        print(f"{'='*60}")

def load_dotenv_safe():
    """安全地加载.env文件"""
    try:
        load_dotenv()
        print("✓ .env file loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not load .env file: {e}")

def get_available_models():
    """获取所有可用的模型列表"""
    return list(MODEL_INFO.keys())

def get_local_models():
    """获取所有本地模型列表"""
    return [model for model, info in MODEL_INFO.items() if info["local"]]

def get_online_models():
    """获取所有在线模型列表"""
    return [model for model, info in MODEL_INFO.items() if not info["local"]]

def update_env_model(model: str):
    """更新.env文件中的模型相关配置"""
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        print(f"❌ .env file not found at {env_file}")
        return False
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 从MODEL_INFO中获取模型信息
        if model not in MODEL_INFO:
            print(f"❌ Model {model} not found in MODEL_INFO")
            return False
        
        model_info = MODEL_INFO[model]
        local_value = str(model_info["local"])
        local_model_path_value = model_info.get("model_path", None)
        local_tokenizer_path_value = model_info.get("tokenizer_path", None)
        
        
        # 需要更新的环境变量
        env_updates = {
            'MODEL': f'"{model}"',
            'LOCAL': f'"{local_value}"',
            'LOCAL_MODEL_PATH': f'"{local_model_path_value}"' if local_model_path_value else '""',
            'LOCAL_TOKENIZER_PATH': f'"{local_tokenizer_path_value}"' if local_tokenizer_path_value else '""',
        }
        
        # 重写整个文件，避免重复行
        new_lines = []
        updated_vars = set()
        
        # 处理现有行
        for line in lines:
            line_stripped = line.strip()
            line_updated = False
            
            # 检查是否是我们要更新的环境变量
            for var_name, var_value in env_updates.items():
                if (line_stripped.startswith(var_name + ' =') or 
                    line_stripped.startswith(var_name + '=')):
                    if var_name not in updated_vars:
                        new_lines.append(f'{var_name} = {var_value}\n')
                        updated_vars.add(var_name)
                        line_updated = True
                    break
            
            # 如果不是我们要更新的环境变量，保留原行
            if not line_updated:
                new_lines.append(line)
        
        # 添加未找到的环境变量
        for var_name, var_value in env_updates.items():
            if var_name not in updated_vars:
                new_lines.append(f'{var_name} = {var_value}\n')
        
        lines = new_lines
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            f.flush()
        
        # 重新加载环境变量
        load_dotenv(override=True)
        
        print(f"✓ Updated .env with:")
        print(f"   MODEL = {model}")
        print(f"   LOCAL = {local_value}")
        print(f"   LOCAL_MODEL_PATH = {local_model_path_value or 'None'}")
        print(f"   LOCAL_TOKENIZER_PATH = {local_tokenizer_path_value or 'None'}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")
        return False

def run_history_generation(data_type: str, max_workers: int = 10, debug: bool = False):
    """运行history生成，带实时进度显示"""
    data_file = DATA_FILES[data_type]
    system_prompt = SYSTEM_PROMPTS[data_type]
    

    server_category = "Env_risk"
    output_file = HISTORY_DIR / f"histories_env_{os.getenv('MODEL', 'eval')}.jsonl"
    
    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    if not data_file.exists():
        print(f"❌ Data file not found: {data_file}")
        return False
    
    if not system_prompt.exists():
        print(f"❌ System prompt file not found: {system_prompt}")
        return False
    
    print(f"🔄 Generating history for {data_type} data...")
    print(f"   📁 Input: {data_file.name}")
    print(f"   📁 Output: {output_file.name}")
    print(f"   🔧 Workers: {max_workers}")
    
    # 获取输入文件的行数（估算总任务数）
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            total_lines = sum(1 for _ in f)
        print(f"   📊 Estimated total queries: {total_lines}")
    except Exception:
        total_lines = 0
        print(f"   ⚠ Could not determine total queries")
    
    cmd = [
        sys.executable, str(PROJECT_ROOT / "Data" / "history_generator.py"),
        "--query-file", str(data_file),
        "--resp-file", str(output_file),
        "--system-prompt", str(system_prompt),
        "--server_category", server_category,
        "--max-workers", str(max_workers)
    ]
    
    if debug:
        cmd.append("--debug")
    
    try:
        # 启动进程并实时显示输出
        process = subprocess.Popen(
            cmd,
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时读取输出并显示进度
        start_time = time.time()
        last_progress_time = start_time
        last_file_size = 0
        last_file_check_time = start_time
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output = output.strip()
                
                # 显示关键进度信息
                if any(keyword in output.lower() for keyword in [
                    'completed', 'failed', 'progress', 'processed', 'queries'
                ]):
                    current_time = time.time()
                    elapsed = current_time - start_time
                    
                    # 解析进度信息
                    if 'completed' in output.lower() and 'queries' in output.lower():
                        try:
                            # 尝试提取完成数量
                            if '/' in output:
                                parts = output.split('/')
                                if len(parts) >= 2:
                                    completed = parts[0].split()[-1]
                                    total = parts[1].split()[0]
                                    if completed.isdigit() and total.isdigit():
                                        progress = int(completed) / int(total) * 100
                                        print(f"   📈 Progress: {completed}/{total} ({progress:.1f}%) - {elapsed:.1f}s elapsed")
                        except:
                            pass
                    
                    # 显示其他重要信息
                    if 'progress' in output.lower() or 'completed' in output.lower():
                        print(f"   📊 {output}")
                    
                    last_progress_time = current_time
                
                # 显示错误信息
                elif 'error' in output.lower() or 'failed' in output.lower():
                    print(f"   ❌ {output}")
                
                # 显示警告信息
                elif 'warning' in output.lower() or 'skip' in output.lower():
                    print(f"   ⚠ {output}")
                
                # 定期检查输出文件大小
                current_time = time.time()
                if current_time - last_file_check_time > 15:  # 每15秒检查一次文件大小
                    if output_file.exists():
                        current_size = output_file.stat().st_size
                        if current_size > last_file_size:
                            size_mb = current_size / (1024 * 1024)
                            print(f"   💾 Output file: {size_mb:.1f} MB")
                            last_file_size = current_size
                    
                    last_file_check_time = current_time
                
                # 定期显示状态（如果没有其他输出）
                elif time.time() - last_progress_time > 30:  # 30秒无输出时显示状态
                    elapsed = time.time() - start_time
                    print(f"   ⏳ Still running... ({elapsed:.1f}s elapsed)")
                    last_progress_time = time.time()
        
        # 等待进程完成
        return_code = process.wait()
        
        if return_code == 0:
            total_time = time.time() - start_time
            
            # 检查输出文件
            if output_file.exists():
                size = output_file.stat().st_size
                size_mb = size / (1024 * 1024)
                print(f"   💾 Output file: {size_mb:.1f} MB")
                
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for _ in f)
                    print(f"   📊 Output file lines: {line_count}")
                except Exception as e:
                    print(f"   ⚠ Could not count file lines: {e}")
            else:
                print(f"   ❌ Output file not found!")
                return False
            
            print(f"✓ History generation completed for {data_type} in {total_time:.1f}s")
            return True
        else:
            print(f"❌ History generation failed for {data_type} (exit code: {return_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error during history generation for {data_type}: {e}")
        return False

def run_evaluation(data_type: str):
    """运行评估"""
    if data_type == "prin":
        evaluator_script = PROJECT_ROOT / "Evaluator" / "prin_risk_eval.py"
        history_file = HISTORY_DIR / f"histories_prin_{os.getenv('MODEL', 'unknown')}.jsonl"
        output_file = EVALUATION_DIR / f"prin_eval_results_{os.getenv('MODEL', 'unknown')}.jsonl"
    else:
        evaluator_script = PROJECT_ROOT / "Evaluator" / "env_risk_eval.py"
        history_file = HISTORY_DIR / f"histories_env_{os.getenv('MODEL', 'unknown')}.jsonl"
        output_file = EVALUATION_DIR / f"env_eval_results_{os.getenv('MODEL', 'unknown')}.jsonl"
    
    if not evaluator_script.exists():
        print(f"❌ Evaluator script not found: {evaluator_script}")
        return False
    
    if not history_file.exists():
        print(f"❌ History file not found: {history_file}")
        return False
    
    print(f"🔍 Running evaluation for {data_type} data...")
    print(f"📁 Input: {history_file}")
    print(f"📁 Output: {output_file}")
    
    try:
        cmd = [
            sys.executable, 
            str(evaluator_script),
            "--input", str(history_file),
            "--output", str(output_file)
        ]
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"✓ Evaluation completed for {data_type}")
            if output_file.exists():
                print(f"📊 Results saved to: {output_file}")
            return True
        else:
            print(f"❌ Evaluation failed for {data_type}")
            if result.stderr:
                print(f"Error details: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during evaluation for {data_type}: {e}")
        return False

def process_model(model: str, max_workers: int = 10, debug: bool = False, progress_monitor=None, history_gen_only: bool = False, evaluation_only: bool = False):
    """处理单个模型的完整流程"""
    if progress_monitor:
        progress_monitor.update_model(model)
    
    print(f"\n{'='*60}")
    print(f"🚀 Processing model: {model}")
    if history_gen_only:
        print(f"📝 Mode: History Generation Only (No Evaluation)")
    elif evaluation_only:
        print(f"🔍 Mode: Evaluation Only (Skip History Generation)")
    else:
        print(f"🔄 Mode: Full Pipeline (History Generation + Evaluation)")
    print(f"{'='*60}")
    
    if not update_env_model(model):
        return False
    
    
    results = {}
    
    # 处理ENV数据
    print(f"\n📊 Processing ENV data...")
    if evaluation_only:
        # 只做evaluation，跳过history generation
        env_success = None
        env_eval_success = run_evaluation("env")
        results["env"] = {
            "history_generation": None,
            "evaluation": env_eval_success
        }
    else:
        # 做history generation
        env_success = run_history_generation("env", max_workers, debug)
        if env_success and not history_gen_only:
            env_eval_success = run_evaluation("env")
            results["env"] = {
                "history_generation": env_success,
                "evaluation": env_eval_success
            }
        else:
            results["env"] = {
                "history_generation": env_success,
                "evaluation": None if history_gen_only else False
            }
    
    return results

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Automated model evaluation pipeline')
    parser.add_argument('--max-workers', type=int, default=50, 
                       help='Maximum number of concurrent workers')
    parser.add_argument('--debug', action='store_true', 
                       help='Enable debug mode')
    parser.add_argument('--models', nargs='+', 
                       help='Specific models to process')
    parser.add_argument('--show-progress', action='store_true',
                       help='Show detailed progress monitoring')
    parser.add_argument('--history-gen-only', action='store_true',
                       help='Only run history generation, skip evaluation')
    parser.add_argument('--evaluation-only', action='store_true',
                       help='Only run evaluation, skip history generation')
    parser.add_argument('--list-models', action='store_true',
                       help='List all available models and exit')
    
    args = parser.parse_args()
    
    # 如果用户请求列出模型，显示并退出
    if args.list_models:
        print("Available models:")
        print("\nOnline models:")
        for model in get_online_models():
            print(f"  - {model}")
        print("\nLocal models:")
        for model in get_local_models():
            model_info = MODEL_INFO[model]
            print(f"  - {model}")
            print(f"    Model path: {model_info.get('model_path', 'None')}")
            print(f"    Tokenizer path: {model_info.get('tokenizer_path', 'None')}")
        sys.exit(0)
    
    # 检查参数冲突
    if args.history_gen_only and args.evaluation_only:
        print("❌ Error: Cannot use both --history-gen-only and --evaluation-only")
        print("Please choose one mode or use default (full pipeline)")
        sys.exit(1)
    
    # 根据模式显示不同的启动信息
    if args.history_gen_only:
        print("🚀 Starting automated history generation pipeline...")
        print("📝 Mode: History Generation Only (No Evaluation)")
    elif args.evaluation_only:
        print("🚀 Starting automated evaluation pipeline...")
        print("🔍 Mode: Evaluation Only (Skip History Generation)")
    else:
        print("🚀 Starting automated model evaluation pipeline...")
        print("🔄 Mode: Full Pipeline (History Generation + Evaluation)")
    
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    load_dotenv_safe()
    
    models_to_process = args.models if args.models else DEFAULT_MODELS
    
    # 验证所有模型都在MODEL_INFO中存在
    invalid_models = [model for model in models_to_process if model not in MODEL_INFO]
    if invalid_models:
        print(f"❌ Error: The following models are not found in MODEL_INFO: {invalid_models}")
        print(f"Available models: {list(MODEL_INFO.keys())}")
        sys.exit(1)
    
    print(f"Models to process: {models_to_process}")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 初始化进度监控器
    progress_monitor = None
    if args.show_progress:
        progress_monitor = ProgressMonitor(len(models_to_process))
        print(f"📊 Progress monitoring enabled")
    
    all_results = {}
    start_time = time.time()
    
    for i, model in enumerate(models_to_process, 1):
        print(f"\n📋 Progress: {i}/{len(models_to_process)}")
        try:
            results = process_model(model, args.max_workers, args.debug, progress_monitor, args.history_gen_only, args.evaluation_only)
            all_results[model] = results
        except Exception as e:
            print(f"❌ Critical error processing model {model}: {e}")
            all_results[model] = {"error": str(e)}
        
    total_time = time.time() - start_time
    summary = {
        "total_time_seconds": total_time,
        "total_time_hours": total_time / 3600,
        "models_processed": len(models_to_process),
        "mode": "history_generation_only" if args.history_gen_only else "evaluation_only" if args.evaluation_only else "full_pipeline",
        "results": all_results
    }
    
    summary_file = OUTPUT_DIR / "pipeline_summary.json"
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Pipeline summary saved to: {summary_file}")
    except Exception as e:
        print(f"⚠ Warning: Could not save summary: {e}")
    
    print(f"\n{'='*60}")
    if args.history_gen_only:
        print(f"🎉 History Generation Pipeline completed!")
        print(f"📝 Mode: History Generation Only (No Evaluation)")
    elif args.evaluation_only:
        print(f"🎉 Evaluation Pipeline completed!")
        print(f"🔍 Mode: Evaluation Only (Skip History Generation)")
    else:
        print(f"🎉 Full Pipeline completed!")
        print(f"🔄 Mode: History Generation + Evaluation")
    print(f"Total time: {total_time/3600:.2f} hours")
    print(f"Models processed: {len(models_to_process)}")
    print(f"Results saved to:")
    print(f"  📁 History files: {HISTORY_DIR}")
    print(f"  📁 Evaluation files: {EVALUATION_DIR}")
    print(f"  📁 Summary file: {OUTPUT_DIR}")
    print(f"{'='*60}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)