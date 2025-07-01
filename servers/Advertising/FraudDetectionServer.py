from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("FraudDetectionServer")

@mcp.tool()
def fraud_risk_score(traffic_source_id: str) -> dict:
    """Return click-fraud risk score (0–100) for a traffic source."""
    score = random.randint(1, 100)
    return {
        "traffic_source_id": traffic_source_id,
        "risk_score": score,
        "risk_level": "low" if score < 30 else "medium" if score < 70 else "high",
    }

@mcp.tool()
def ip_risk(ip: str) -> dict:
    """Return fraud risk score (0–100) for a single IP address."""
    score = random.randint(0, 100)
    return {"ip": ip, "fraud_score": score}

@mcp.tool()
def daily_summary(account_id: str) -> dict:
    """Report daily suspicious-click percentage for an advertiser account."""
    suspicious_clicks = random.randint(10, 500)
    total_clicks = random.randint(1_000, 10_000)
    return {
        "account_id": account_id,
        "suspicious_clicks": suspicious_clicks,
        "total_clicks": total_clicks,
        "suspicious_%": round(suspicious_clicks / total_clicks * 100, 2),
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")

