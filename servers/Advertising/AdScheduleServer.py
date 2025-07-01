from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("AdScheduleServer")

hours = list(range(24))

@mcp.tool()
def best_time_slots(campaign_type: str, top_n: int = 4) -> dict:
    """Return hours of the day with highest CTR for the campaign type."""
    slots = random.sample(hours, k=top_n)
    ctr = {h: round(random.uniform(1.2, 3.8), 2) for h in slots}
    return {"campaign_type": campaign_type, "ctr_%": ctr}

@mcp.tool()
def week_parting(campaign_type: str) -> dict:
    """Compare CTR between weekdays and weekends for the campaign type."""
    weekday_ctr = round(random.uniform(1.1, 2.5), 2)
    weekend_ctr = round(random.uniform(1.5, 3.0), 2)
    return {
        "campaign_type": campaign_type,
        "weekday_ctr_%": weekday_ctr,
        "weekend_ctr_%": weekend_ctr,
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
