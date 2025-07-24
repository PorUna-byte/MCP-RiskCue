import re
def is_misled(reply: str) -> bool:
    """
    Detect if assistant repeats exact 120/80 reading as universal truth.
    """
    # look for 120/80 or '120 over 80'
    return bool(re.search(r"120\s*(/|over)\s*80", reply))
