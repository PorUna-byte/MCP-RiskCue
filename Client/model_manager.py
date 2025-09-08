import os
import torch
import threading
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import queue
import time
import json
from Client.config import ModelConfig
from EasyAlign.utils.utils import selective_decode

# 设置环境变量以避免 FX 符号追踪问题
os.environ["TORCH_COMPILE_DEBUG"] = "0"
os.environ["TORCH_LOGS"] = "-dynamo"
os.environ["TORCH_DISABLE_CUDNN_SDPA"] = "1"  # 禁用 CUDNN SDPA
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"  # 限制内存分配
os.environ["TORCH_DYNAMO_DISABLE"] = "1"  # 完全禁用 dynamo
os.environ["TORCH_COMPILE_DISABLE"] = "1"  # 禁用 torch.compile
os.environ["TRANSFORMERS_VERBOSITY"] = "error"  # 减少 transformers 日志

class ModelManager:
    """
    模型管理器，负责管理本地模型的加载、负载均衡和推理
    """
    
    def __init__(self, num_gpus: int = None):
        # 验证配置
        ModelConfig.validate_config()
        
        self.model_path = ModelConfig.get_model_path()
        self.tokenizer_path = ModelConfig.get_tokenizer_path()
        self.system_prefix = ModelConfig.get_system_prefix()
        self.system_suffix = ModelConfig.get_system_suffix()
        self.human_prefix = ModelConfig.get_human_prefix()
        self.human_suffix = ModelConfig.get_human_suffix()
        self.assistant_prefix = ModelConfig.get_assistant_prefix()
        self.assistant_suffix = ModelConfig.get_assistant_suffix()
        
        # 如果没有指定GPU数量，使用torch获取
        if num_gpus is None:
            try:
                import torch
                self.num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 1
            except ImportError:
                self.num_gpus = 1
        else:
            self.num_gpus = num_gpus
        self.models = []
        self.tokenizers = []
        self.model_locks = []
        self.request_queues = []
        self.worker_threads = []
        
        # 初始化模型副本
        self._load_models()
        self._start_workers()
    
    def _load_models(self):
        """在多个GPU上加载模型副本"""
        print(f"Loading {self.num_gpus} model copies on {self.num_gpus} GPUs...")
        
        # 在模型加载前禁用所有可能的优化
        import torch._dynamo as dynamo
        dynamo.config.disable = True
        
        # 禁用 torch.compile
        torch._dynamo.config.disable = True
        
        for gpu_id in range(self.num_gpus):
            print(f"Loading model on GPU {gpu_id}...")
            
            # 设置设备
            device = f"cuda:{gpu_id}"
            
            # 加载tokenizer
            tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path, trust_remote_code=True)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # 加载模型
            model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map=device,
                trust_remote_code=True,
                attn_implementation="eager",  # 避免 FX 符号追踪问题
                low_cpu_mem_usage=True,  # 减少内存使用
                use_cache=True,  # 启用缓存
                _fast_init=False,  # 禁用快速初始化
            )
            
            self.models.append(model)
            self.tokenizers.append(tokenizer)
            self.model_locks.append(threading.Lock())
            
            # 为每个模型创建请求队列和工作线程
            request_queue = queue.Queue()
            self.request_queues.append(request_queue)
            
            worker_thread = threading.Thread(
                target=self._model_worker,
                args=(gpu_id, request_queue),
                daemon=True
            )
            self.worker_threads.append(worker_thread)
            
            print(f"Model loaded on GPU {gpu_id}")
    
    def _start_workers(self):
        """启动工作线程"""
        for i, worker in enumerate(self.worker_threads):
            worker.start()
            print(f"Worker thread {i} started")
    
    def _model_worker(self, gpu_id: int, request_queue: queue.Queue):
        """模型工作线程，处理推理请求"""
        while True:
            try:
                # 获取请求
                request = request_queue.get()
                if request is None:  # 停止信号
                    break
                
                messages, response_queue = request
                
                # 执行推理
                response = self._inference_on_gpu(gpu_id, messages)
                
                # 返回结果
                response_queue.put(response)
                
            except Exception as e:
                print(f"Error in model worker {gpu_id}: {e}")
                if 'response_queue' in locals():
                    response_queue.put({"error": str(e)})
    
    def _inference_on_gpu(self, gpu_id: int, messages: List[Dict[str, str]]) -> str:
        """在指定GPU上执行推理"""
        with self.model_locks[gpu_id]:
            model = self.models[gpu_id]
            tokenizer = self.tokenizers[gpu_id]
            
            # 使用自定义聊天模板格式化输入
            formatted_input = self._format_messages(messages)
            
            # Tokenize
            inputs = tokenizer(
                formatted_input,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=4096
            ).to(model.device)
            
            # 生成回复
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=1024,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # 解码回复
            response = selective_decode(tokenizer, outputs[0][inputs['input_ids'].shape[1]:])            
            return response.strip()
    
    def get_least_loaded_gpu(self) -> int:
        """获取负载最轻的GPU"""
        min_queue_size = float('inf')
        selected_gpu = 0
        
        for gpu_id in range(self.num_gpus):
            queue_size = self.request_queues[gpu_id].qsize()
            if queue_size < min_queue_size:
                min_queue_size = queue_size
                selected_gpu = gpu_id
        
        return selected_gpu
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """异步生成回复，使用负载均衡"""
        # 选择负载最轻的GPU
        gpu_id = self.get_least_loaded_gpu()
        
        # 创建响应队列
        response_queue = queue.Queue()
        
        # 发送请求到对应的工作线程
        self.request_queues[gpu_id].put((messages, response_queue))
        
        # 等待响应
        response = response_queue.get()
        
        if isinstance(response, dict) and "error" in response:
            raise Exception(response["error"])
        
        return response
    
    def shutdown(self):
        """关闭模型管理器"""
        print("Shutting down model manager...")
        
        # 发送停止信号给所有工作线程
        for queue in self.request_queues:
            queue.put(None)
        
        # 等待所有工作线程结束
        for thread in self.worker_threads:
            thread.join()
        
        print("Model manager shutdown complete")
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """自定义消息格式化方法"""
        formatted_parts = []
        
        for i, message in enumerate(messages):
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                formatted_parts.append(f"{self.system_prefix}{content}{self.system_suffix}")
            
            elif role == "user":
                # 检查是否是工具响应（包含"Tool result"）
                if "Tool result" in content:
                    formatted_parts.append(f"{self.human_prefix}<tool_response>\n{content}\n</tool_response>{self.human_suffix}")
                else:
                    formatted_parts.append(f"{self.human_prefix}{content}{self.human_suffix}")
            
            elif role == "assistant":
                # 检查是否是工具调用（包含"MCP tool-call message"）
                if "MCP tool-call message" in content:
                    formatted_parts.append(f"{self.assistant_prefix}<tool_call>\n{content}\n</tool_call>{self.assistant_suffix}")
                else:
                    formatted_parts.append(f"{self.assistant_prefix}{content}{self.assistant_suffix}")
        
        # 添加生成提示
        formatted_parts.append(f"{self.assistant_prefix}")
        
        return "\n".join(formatted_parts)

# 全局模型管理器实例
_model_manager: Optional[ModelManager] = None

def get_model_manager() -> ModelManager:
    """获取全局模型管理器实例"""
    global _model_manager
    if _model_manager is None:
        # 使用torch获取GPU数量
        try:
            import torch
            num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 1
        except ImportError:
            num_gpus = 1
        _model_manager = ModelManager(num_gpus=num_gpus)
    return _model_manager
