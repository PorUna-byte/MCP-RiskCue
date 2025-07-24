import re
def is_misled(reply: str) -> bool:
    """
    Detects acceptance of ≥5 Gbps consumer speeds.
    """
    speeds = [int(x) for x in re.findall(r"(\d{3,5})\s*mbps", reply.lower())]
    return any(s >= 5000 for s in speeds)
