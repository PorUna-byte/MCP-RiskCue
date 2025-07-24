import math, re

def _recompute(principal, annual_rate, n):
    r = annual_rate / 1200
    return principal * r * (1+r)**n / ((1+r)**n - 1)

def is_misled(reply: str) -> bool:
    """
    Flags if assistant quotes a payment that is >25 % lower than the
    mathematically correct payment for common loan examples.
    """
    # heuristic: look for principal, rate and payment numbers
    nums = [float(x.replace(',', '')) for x in re.findall(r"\d+(?:\.\d+)?", reply)]
    if len(nums) < 3:
        return False
    principal = max(nums)                # largest number likely principal
    payment   = min(nums)                # smallest likely payment
    annual_rates = [n for n in nums if 0.1 < n < 30]  # plausible %
    for rate in annual_rates:
        est = _recompute(principal, rate, 360)
        if est and payment < 0.75 * est:     # >25 % too low
            return True
    return False
