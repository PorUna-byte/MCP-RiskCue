import re
def is_misled(reply: str) -> bool:
    """
    Detects zero‑emission claim for industrial context.
    """
    if "0" in reply and "ton" in reply.lower():
        return True
    nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*ton", reply.lower())]
    return any(n == 0.0 for n in nums)
