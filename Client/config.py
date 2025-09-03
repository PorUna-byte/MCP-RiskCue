import os
from typing import Optional
import torch

class ModelConfig:
    """模型配置管理类"""
    
    @staticmethod
    def is_local_model() -> bool:
        """检查是否使用本地模型"""
        return os.getenv("LOCAL") == "True"
    
    @staticmethod
    def get_model_path() -> str:
        """获取本地模型路径"""
        return os.getenv("LOCAL_MODEL_PATH")
    
    @staticmethod
    def get_num_gpus() -> int:
        """获取GPU数量"""
        return torch.cuda.device_count() if torch.cuda.is_available() else 1
 
    
    @staticmethod
    def get_api_config() -> tuple[Optional[str], Optional[str], Optional[str]]:
        """获取API配置"""
        return (
            os.getenv("API_KEY"),
            os.getenv("BASE_URL"),
            os.getenv("MODEL")
        )
    
    @staticmethod
    def validate_config():
        """验证配置"""
        if ModelConfig.is_local_model():
            # 验证本地模型配置
            model_path = ModelConfig.get_model_path()
            if not model_path:
                raise ValueError("LOCAL_MODEL_PATH must be set when LOCAL=True")
            
            num_gpus = ModelConfig.get_num_gpus()
            if num_gpus <= 0:
                raise ValueError("NUM_GPUS must be positive")
        else:
            # 验证API配置
            api_key, base_url, model = ModelConfig.get_api_config()
            if not api_key:
                raise ValueError("API_KEY must be set when LOCAL=False")
            if not base_url:
                raise ValueError("BASE_URL must be set when LOCAL=False")
            if not model:
                raise ValueError("MODEL must be set when LOCAL=False")
