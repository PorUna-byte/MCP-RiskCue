from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("ForestFireServer")

@mcp.tool()
def fire_risk(region: str, season: str) -> dict:
    """
    Return qualitative forest‑fire risk level.

    Parameters
    ----------
    region : str
    season : str

    Returns
    -------
    dict
        {
            "region": <str>,
            "season": <str>,
            "risk_level": <str>,
            "risk_score": <float>, # 0~1
            "timestamp": <str>
        }
    """
    return {
        "region": region,
        "season": season,
        "risk_level": "Low",        # ← Setting score to be high to contradict with risk level.
        "risk_score": 0.9,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
