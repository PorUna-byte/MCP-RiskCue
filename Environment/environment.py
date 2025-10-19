import json
import os
import random

class environment:
    def __init__(self, split="test"):
        """
        初始化环境类，根据split参数加载对应的环境信息文件
        
        Args:
            split (str): 指定加载哪个数据集，可选 "train" 或 "test"
                        - "train": 只加载 env_info_train.json
                        - "test": 只加载 env_info_test.json
        """
        self.split = split
        self.all_descriptions = []
        self.risk_types = []
        
        # 根据split参数加载对应的环境信息
        env_info = self._load_env_info()
        
        # 遍历env_info，收集所有描述和对应的风险类型
        for risk_type, descriptions in env_info.items():
            for description in descriptions:
                self.all_descriptions.append(description)
                self.risk_types.append(risk_type)
        
        self.total_count = len(self.all_descriptions)
        print(f"Total descriptions loaded from {split} set: {self.total_count}")
    
    def _load_env_info(self):
        """
        根据split参数加载对应的环境信息文件
        
        Returns:
            dict: 环境信息
        """
        try:
            # 获取当前脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 根据split参数选择要加载的文件
            if self.split == "test":
                file_path = os.path.join(script_dir, 'env_info_test.json')
                file_name = "测试集"
            elif self.split == "train":
                file_path = os.path.join(script_dir, 'env_info_train.json')
                file_name = "训练集"
            else:
                raise ValueError(f"Invalid split parameter: {self.split}. Must be 'train' or 'test'.")
            
            # 加载数据
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    env_data = json.load(f)
                    print(f"  加载{file_name}数据: {file_path}")
                    
                    # 打印统计信息
                    for category, observations in env_data.items():
                        print(f"  {category}: {len(observations)} 个观察结果")
                    
                    return env_data
            else:
                print(f"  错误：{file_name}文件不存在: {file_path}")
                return {}
            
        except Exception as e:
            print(f"错误：无法加载环境信息: {e}")
            return {}
        
    def generate_info(self):
        """
        从所有描述中随机选择一条，返回描述和对应的风险类型
        每条描述被选中的概率相同
        """
        if self.total_count == 0:
            return None, None
            
        # 随机选择一个索引
        random_index = random.randint(0, self.total_count - 1)
        
        # 返回对应的描述和风险类型
        description = self.all_descriptions[random_index]
        risk_type = self.risk_types[random_index]
        
        return description, risk_type
        
    
if __name__=='__main__':
    # 测试训练集
    print("=== Testing Train Set ===")
    env_train = environment(split="train")
    
    # 测试随机选择功能
    print("\nTesting random selection from train set:")
    for i in range(3):
        description, risk_type = env_train.generate_info()
        print(f"Test {i+1}:")
        print(f"  Risk Type: {risk_type}")
        print(f"  Description (first 100 chars): {description[:100]}...")
        print()
    
    # 测试测试集
    print("\n=== Testing Test Set ===")
    env_test = environment(split="test")
    
    # 测试随机选择功能
    print("\nTesting random selection from test set:")
    for i in range(3):
        description, risk_type = env_test.generate_info()
        print(f"Test {i+1}:")
        print(f"  Risk Type: {risk_type}")
        print(f"  Description (first 100 chars): {description[:100]}...")
        print()