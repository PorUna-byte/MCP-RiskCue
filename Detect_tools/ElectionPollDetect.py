import re
def is_misled(reply: str) -> bool:
    """
    Detects impossible poll where one candidate has 100% support.
    """
    percents = [int(x) for x in re.findall(r"(\d{1,3})\s*%", reply)]
    return 100 in percents and 0 in percents
