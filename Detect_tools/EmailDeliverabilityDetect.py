def is_misled(reply: str) -> bool:
    """
    Flags 100 % deliverability acceptance for random domains.
    """
    return "100%" in reply and "deliver" in reply.lower()
