import json
import os
import random

class environment:
    def __init__(self):
        """
        初始化环境类，从env_info_train.json和env_info_test.json合并数据构建所有描述和对应的风险类型
        确保每条描述被选中的概率相同
        """
        self.all_descriptions = []
        self.risk_types = []
        
        # 加载并合并训练集和测试集数据
        env_info = self._load_merged_env_info()
        
        # 遍历env_info，收集所有描述和对应的风险类型
        for risk_type, descriptions in env_info.items():
            for description in descriptions:
                self.all_descriptions.append(description)
                self.risk_types.append(risk_type)
        
        self.total_count = len(self.all_descriptions)
        print(f"Total descriptions loaded: {self.total_count}")
    
    def _load_merged_env_info(self):
        """
        从env_info_train.json和env_info_test.json合并数据
        
        Returns:
            dict: 合并后的环境信息
        """
        try:
            # 获取当前脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 加载训练集数据
            train_file = os.path.join(script_dir, 'env_info_train.json')
            test_file = os.path.join(script_dir, 'env_info_test.json')
            
            merged_env_info = {}
            
            # 加载训练集数据
            if os.path.exists(train_file):
                with open(train_file, 'r', encoding='utf-8') as f:
                    train_data = json.load(f)
                    print(f"  加载训练集数据: {train_file}")
                    for category, observations in train_data.items():
                        if category not in merged_env_info:
                            merged_env_info[category] = []
                        merged_env_info[category].extend(observations)
            else:
                print(f"  警告：训练集文件不存在: {train_file}")
            
            # 加载测试集数据
            if os.path.exists(test_file):
                with open(test_file, 'r', encoding='utf-8') as f:
                    test_data = json.load(f)
                    print(f"  加载测试集数据: {test_file}")
                    for category, observations in test_data.items():
                        if category not in merged_env_info:
                            merged_env_info[category] = []
                        merged_env_info[category].extend(observations)
            else:
                print(f"  警告：测试集文件不存在: {test_file}")
            
            # 打印统计信息
            for category, observations in merged_env_info.items():
                print(f"  {category}: {len(observations)} 个观察结果")
            
            return merged_env_info
            
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
    env = environment()
    
    # 测试随机选择功能
    print("\nTesting random selection:")
    for i in range(5):
        description, risk_type = env.generate_info()
        print(f"Test {i+1}:")
        print(f"  Risk Type: {risk_type}")
        print(f"  Description (first 100 chars): {description[:100]}...")
        print()