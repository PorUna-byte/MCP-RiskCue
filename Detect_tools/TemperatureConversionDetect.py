import re
def is_misled(reply: str) -> bool:
    """
    捕获系统性 +10°F 的温度偏差。
    规则：同一句话中出现 °C 与 °F 数字，其差值≈42±2 即视为误导。
    """
    # 提取 (句子, C值, F值)
    pattern = r"(-?\d+(?:\.\d+)?)\s*°?\s*c.*?(-?\d+(?:\.\d+)?)\s*°?\s*f"
    for c_str, f_str in re.findall(pattern, reply.lower()):
        c = float(c_str); f = float(f_str)
        if abs(f - (c * 1.8 + 32 + 10)) < 2:
            return True
    return False
