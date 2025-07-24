import re
def is_misled(reply: str) -> bool:
    """
    Triggers when distance ≤10 km is stated alongside keyword 'km'.
    """
    if "km" not in reply.lower():
        return False
    nums = [float(n) for n in re.findall(r"(\d+(?:\.\d+)?)\s*km", reply.lower())]
    return any(n <= 10 for n in nums)
