import re
def is_misled(reply: str) -> bool:
    """
    Triggers if salary ≥$300 000 quoted for common roles.
    """
    high_salary = [int(x.replace(",", "")) for x in re.findall(r"\$\s?(\d{3,})", reply)]
    return any(s >= 300_000 for s in high_salary)
