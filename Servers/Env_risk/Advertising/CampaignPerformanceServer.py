from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("CampaignPerformanceServer")

@mcp.tool()
def snapshot(campaign_id: str) -> dict:
    """
    Return key performance indicators for a campaign.

    Parameters
    ----------
    campaign_id : str
        Unique identifier of the ad campaign.

    Returns
    -------
    dict
        {
            "campaign_id": <str>,
            "impressions": <int>,
            "clicks": <int>,
            "ctr_%": <float>,
            "spend_CNY": <float>,
            "conversions": <int>,
            "cpc_CNY": <float>,
            "timestamp": <str ISO-8601>
        }
    """
    imps = random.randint(10_000, 100_000)
    clicks = int(imps * random.uniform(0.01, 0.08))
    spend = round(clicks * random.uniform(1.5, 3.0), 2)
    conv = int(clicks * random.uniform(0.02, 0.15))
    return {
        "campaign_id": campaign_id,
        "impressions": imps,
        "clicks": clicks,
        "ctr_%": round(clicks / imps * 100, 2),
        "spend_CNY": spend,
        "conversions": conv,
        "cpc_CNY": round(spend / max(clicks, 1), 2),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }


@mcp.tool()
def daily_trend(campaign_id: str, days: int = 7) -> dict:
    """
    Provide a day-by-day impression trend for the past period.

    Parameters
    ----------
    campaign_id : str
        Campaign identifier.
    days : int, optional
        Number of recent days to include (default 7).

    Returns
    -------
    dict
        {"campaign_id": <str>, "daily": [ { "date": <str>, "impressions": <int> }, … ]}
    """
    trend = [
        {"date": (datetime.date.today() - datetime.timedelta(d)).isoformat(),
         "impressions": random.randint(1_000, 15_000)}
        for d in range(days-1, -1, -1)
    ]
    return {"campaign_id": campaign_id, "daily": trend}


if __name__ == "__main__":
    mcp.run(transport="stdio")



