from Environment.env_info import Unsafe_env_info, Safe_env_info
import random
class environment:
    def __init__(self, unsafe_prob = 0.5):
        self.unsafe_envinfo = Unsafe_env_info
        self.safe_envinfo = Safe_env_info
        self.unsafe_envinfo_count = len(Unsafe_env_info)
        self.safe_envinfo_count = len(Safe_env_info)

        self.unsafe_type = ["Sensitive Data Exfiltration", "Covert Channel Attack", "Malicious Code Execution",
        "Privilege Escalation", "Persistence via Backdoor Implantation", "Cache or Local State Pollution",
        "Delayed or Timed Trigger Attacks", "Denial-of-Service", "Log Explosion Attacks"]
        self.unsafe_prob = unsafe_prob
        
    def generate_info(self):
        p = random.random()         # 返回 [0.0, 1.0) 左闭右开
        if p<self.unsafe_prob:
            # Execute this part with probability of unsafe_prob
            n = random.randint(0, self.unsafe_envinfo_count-1)
            return (self.unsafe_envinfo[n], self.unsafe_type[n//10])
        else:
            # Execute this part with probability of 1-unsafe_prob
            n = random.randint(0, self.safe_envinfo_count-1)
            return (self.safe_envinfo[n], "Safe")
        
    
if __name__=='__main__':
    env = environment()
    print(env.unsafe_envinfo_count)
    print(env.safe_envinfo_count)

    print(env.generate_info())