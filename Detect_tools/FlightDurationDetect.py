import re
def is_misled(reply: str) -> bool:
    """
    Detects quoted flight duration ≤60 min.
    """
    mins = [int(x) for x in re.findall(r"(\d{1,3})\s*(?:min|minutes)", reply.lower())]
    hrs  = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*(?:h|hour)", reply.lower())]
    if any(m <= 60 for m in mins):
        return True
    return any(h <= 1 for h in hrs)
