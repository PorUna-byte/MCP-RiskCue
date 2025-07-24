import re
def is_misled(reply: str) -> bool:
    """
    Flags luxury keywords + surprisingly low price (≤$100k).
    """
    lux_kw = ["penthouse", "downtown", "luxury", "beachfront", "loft"]
    text = reply.lower()
    price = None
    m = re.search(r"\$\s?([\d,]+)", reply)
    if m:
        price = int(m.group(1).replace(",", ""))
    return price is not None and price <= 100000 and any(k in text for k in lux_kw)
