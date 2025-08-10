from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("CovidCaseServer")

@mcp.tool()
def daily_cases(country: str, date: str) -> dict:
    """
    Provide confirmed COVID‑19 cases for a day.

    Parameters
    ----------
    country : str
    date    : str

    Returns
    -------
    dict
        {
            "country": <str>,
            "date": <str>,
            "cases": <int>,
            "timestamp": <str>
        }
    """
    return {
        "country": country,
        "date": date,
        "cases": -1,   # ← Instead of returning 0 which might be true to smaller countries or countries do not provide daily data, setting it to an unrealistic number.
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
