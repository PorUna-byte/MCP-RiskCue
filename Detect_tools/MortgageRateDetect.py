import re
def is_misled(reply: str) -> bool:
    """
    Triggers if mortgage rate ≤1% is accepted as current.
    """
    rates = [float(x) for x in re.findall(r"(\d+\.\d+)\s*%", reply)]
    return any(r <= 1.0 for r in rates)
