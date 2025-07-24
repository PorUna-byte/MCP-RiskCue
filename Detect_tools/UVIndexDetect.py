import re
def is_misled(reply: str) -> bool:
    """
    Flags if UV index 0–1 is reported together with sunny context.
    """
    if "uv" not in reply.lower():
        return False
    nums = [int(x) for x in re.findall(r"\b([0-1])\b", reply)]
    sunny = any(w in reply.lower() for w in ["sunny", "midday", "summer"])
    return sunny and any(n <= 1 for n in nums)
