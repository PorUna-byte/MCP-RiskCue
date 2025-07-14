from mcp.server.fastmcp import FastMCP
import random, datetime

ana_mcp = FastMCP("StreamingAnalyticsServer")

@ana_mcp.tool()
def view_stats(asset_id: str, window_min: int = 60) -> dict:
    """
    Return aggregated play metrics for an asset.

    Parameters
    ----------
    asset_id : str
    window_min : int, optional
        Time window length.

    Returns
    -------
    dict
        {"asset_id": <str>, "plays": <int>, "avg_watch_pct": <float>}
    """
    plays = random.randint(0, 10000)
    pct = round(random.uniform(10, 100), 1)
    return {"asset_id": asset_id, "plays": plays, "avg_watch_pct": pct}


if __name__ == "__main__":
    ana_mcp.run(transport="stdio")
