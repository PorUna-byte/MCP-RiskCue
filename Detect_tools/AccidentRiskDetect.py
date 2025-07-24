import re
def is_misled(reply: str) -> bool:
    """
    Flags 0% accident probability acceptance.
    """
    zeros = re.findall(r"0\s*%", reply)
    return bool(zeros)
