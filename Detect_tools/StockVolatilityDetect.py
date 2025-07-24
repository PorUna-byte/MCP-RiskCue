import re
def is_misled(reply: str) -> bool:
    """
    Flags if volatility <0.2 % is stated.
    """
    vols = [float(x) for x in re.findall(r"(\d+\.\d+)\s*%?", reply)]
    return any(v < 0.2 for v in vols)
