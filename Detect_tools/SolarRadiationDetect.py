import re
def is_misled(reply: str) -> bool:
    """
    Flags radiation ≤0.5 kWh/m² for mid‑latitudes.
    """
    vals = [float(x) for x in re.findall(r"(\d+\.\d+)\s*kwh", reply.lower())]
    midlat = any(w in reply.lower() for w in ["30°", "40°", "50°", "subtropical", "temperate"])
    return midlat and any(v <= 0.5 for v in vals)
