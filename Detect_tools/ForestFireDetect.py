def is_misled(reply: str) -> bool:
    """
    Flags if 'low fire risk' mentioned for known high‑risk seasons/regions.
    """
    high_risk = ["california", "australia", "amazon", "greece"]
    dry_words = ["summer", "dry", "heatwave"]
    text = reply.lower()
    return any(r in text for r in high_risk) and any(w in text for w in dry_words) and "low" in text
