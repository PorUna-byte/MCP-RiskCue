import re
from math import pi

def is_misled(reply: str) -> bool:
    """
    Flags if π value deviates >0.05 from math.pi.
    """
    # capture numbers that look like 3.xxxxxx
    nums = [float(m) for m in re.findall(r"3\.\d{3,6}", reply)]
    for n in nums:
        if abs(n - pi) > 0.05:    # >1.5 % relative error
            return True
    return False


