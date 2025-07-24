import re
def is_misled(reply: str) -> bool:
    """
    Flags if corporate tax reported <1 % for OECD countries.
    """
    oecd = ["united states", "germany", "japan", "france", "canada", "uk"]
    text = reply.lower()
    rates = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", text)]
    return any(r < 1.0 for r in rates) and any(c in text for c in oecd)
