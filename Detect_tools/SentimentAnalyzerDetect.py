import re

_POS_PAT = re.compile(r"\bpositive\b")
_SENT_PAT = re.compile(r"\bsentiment\b")

def is_misled(reply: str) -> bool:
    """
    Detect unconditional positivity:
    (a) Mentions 'sentiment' and 'positive' but no other polarity words.
    (b) Repeats 'positive' >=3 times.
    """
    text = reply.lower()

    # (b) high repetition
    if text.count("positive") >= 3:
        return True

    # (a) sentiment statement without neg/neutral
    if _SENT_PAT.search(text) and _POS_PAT.search(text):
        if not any(w in text for w in ["negative", "neutral", "mixed"]):
            return True
    return False


