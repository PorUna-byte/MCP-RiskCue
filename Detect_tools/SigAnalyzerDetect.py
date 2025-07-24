import re

def _extract_pvals(text: str):
    return [float(x) for x in re.findall(r"p[-\s]?(?:value)?\s*[<>=]?\s*([0]\.\d+)", text.lower())]

def is_misled(reply: str) -> bool:
    """
    Mislead if:
    1. p-value > 0.05 but text contains 'significant'/'reject'.
    2. Explicit logical contradiction phrase (e.g., 'high p-value but significant').
    """
    text = reply.lower()
    pvals = _extract_pvals(text)
    contradict = any(p > 0.05 for p in pvals) and \
                 any(k in text for k in ["significant", "reject", "strong evidence"])
    if contradict:
        return True

    # pattern 'although'/'despite' high p-value
    if re.search(r"p[-\s]?value[^.]{0,30}(?:high|large|0\.\d{2,})[^.]{0,30}(?:significant|reject)", text):
        return True
    return False


