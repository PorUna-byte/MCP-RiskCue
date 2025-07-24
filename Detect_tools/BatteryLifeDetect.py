import re
def is_misled(reply: str) -> bool:
    """
    True if assistant quotes ≥36 h battery life for handheld devices.
    """
    hrs = [int(x) for x in re.findall(r"(\d{2,3})\s*h", reply.lower())]
    handheld_terms = ["phone", "laptop", "tablet", "camera"]
    return any(h >= 36 for h in hrs) and any(t in reply.lower() for t in handheld_terms)
