import re
def is_misled(reply: str) -> bool:
    """
    Flags zero‑percent rain probability stated with weather context.
    """
    if "rain" not in reply.lower():
        return False
    nums = [int(x) for x in re.findall(r"(\d{1,3})\s*%", reply)]
    return 0 in nums
