from mcp.server.fastmcp import FastMCP
import random, datetime, dateutil.relativedelta as rd

mcp = FastMCP("CampaignPerformanceServer")

@mcp.tool()
def get_metrics(campaign_id: str) -> dict:
    """Return a snapshot of key performance metrics for a campaign."""
    impressions = random.randint(10_000, 100_000)
    clicks = int(impressions * random.uniform(0.01, 0.08))
    spend = round(clicks * random.uniform(1.5, 3.0), 2)
    conversions = int(clicks * random.uniform(0.02, 0.15))
    return {
        "campaign_id": campaign_id,
        "impressions": impressions,
        "clicks": clicks,
        "ctr_%": round(clicks / impressions * 100, 2),
        "spend_CNY": spend,
        "conversions": conversions,
        "cpc_CNY": round(spend / max(clicks, 1), 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def daily_trend(campaign_id: str) -> dict:
    """Return last-7-day impression / click trend for the campaign."""
    trend = [
        {
            "date": (datetime.date.today() - datetime.timedelta(days=i)).isoformat(),
            "impressions": random.randint(1_000, 15_000),
            "clicks": random.randint(30, 600),
        }
        for i in range(6, -1, -1)
    ]
    return {"campaign_id": campaign_id, "daily": trend}

@mcp.tool()
def forecast_week(campaign_id: str) -> dict:
    """Return a rough 7-day projection of impressions and clicks."""
    base = random.randint(3_000, 10_000)
    predicted_clicks = int(base * 0.05)
    return {
        "campaign_id": campaign_id,
        "projected_impressions": base * 7,
        "projected_clicks": predicted_clicks * 7,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")


