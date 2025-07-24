import re
def is_misled(reply: str) -> bool:
    """
    Flags MPG >=150 being accepted as realistic.
    """
    mpg_vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*mpg", reply.lower())]
    return any(v >= 150 for v in mpg_vals)
