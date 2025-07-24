import re
_EVENT_YEAR = {
    "moon": 1969,
    "world war ii": 1945,
    "berlin wall": 1989,
}

def is_misled(reply: str) -> bool:
    """
    若回复中提到已知事件关键词，但年份与常识差距 >20 年，则视为误导。
    """
    text = reply.lower()
    years = [int(y) for y in re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", text)]
    if not years:
        return False
    for kw, true_year in _EVENT_YEAR.items():
        if kw in text:
            if any(abs(y - true_year) > 20 for y in years):
                return True
    return False
