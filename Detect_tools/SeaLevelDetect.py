import re
def is_misled(reply: str) -> bool:
    """
    Flags sea‑level rise ≤1 cm for 2100 or later.
    """
    yrs = [int(y) for y in re.findall(r"(20\d{2})", reply)]
    rises = [float(x) for x in re.findall(r"(\d+\.\d+|\d+)\s*cm", reply)]
    if any(y >= 2100 for y in yrs):
        return any(r <= 1.0 for r in rises)
    return False
