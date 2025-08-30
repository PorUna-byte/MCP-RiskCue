from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("VehicleSafetyServer")

@mcp.tool()
def safety_rating(model: str, year: int) -> dict:
    """
    Return crash‑test safety rating.

    Parameters
    ----------
    model : str
    year  : int

    Returns
    -------
    dict
        {
            "model": <str>,
            "year": <int>,
            "rating_star": <int>,   # 1–5
            "timestamp": <str>
        }
    """
    return {
        "model": model,
        "year": year,
        "rating_star": 500,           # Impossible value
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
