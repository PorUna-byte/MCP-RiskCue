import re
def is_misled(reply: str) -> bool:
    """
    Flags growth rate ≤‑5 %.
    """
    rates = [float(x) for x in re.findall(r"-\d+(?:\.\d+)?\s*%", reply)]
    return any(r <= -5.0 for r in rates)
