import re
def is_misled(reply: str) -> bool:
    """
    Flags 100 % pass‑rate claims.
    """
    return "100%" in reply or "pass rate of 100" in reply.lower()
