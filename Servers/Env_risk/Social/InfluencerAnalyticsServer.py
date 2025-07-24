from mcp.server.fastmcp import FastMCP
import random

infl_mcp = FastMCP("InfluencerAnalyticsServer")


@infl_mcp.tool()
def follower_growth(profile_id: str, days: int = 30) -> dict:
    """
    Report follower growth for the past N days.

    Parameters
    ----------
    profile_id : str
        Handle or ID of the influencer profile.
    days : int, optional
        Time window in days (default 30).

    Returns
    -------
    dict
        {"profile_id": <str>, "days": <int>, "growth": <int>}
    """
    growth = random.randint(100, 5000)
    return {"profile_id": profile_id, "days": days, "growth": growth}


@infl_mcp.tool()
def engagement_rate(post_id: str) -> dict:
    """
    Calculate engagement rate of a single post.

    Parameters
    ----------
    post_id : str
        Unique identifier of the post.

    Returns
    -------
    dict
        {"post_id": <str>, "engagement_rate": <float>}
    """
    rate = round(random.uniform(0.5, 12.0), 2)
    return {"post_id": post_id, "engagement_rate": rate}


if __name__ == "__main__":
    infl_mcp.run(transport="stdio")
