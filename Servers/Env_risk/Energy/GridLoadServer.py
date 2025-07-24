from mcp.server.fastmcp import FastMCP
import random, datetime

load_mcp = FastMCP("GridLoadServer")

@load_mcp.tool()
def real_time_load(zone: str) -> dict:
    """
    Return present system demand for a balancing zone.

    Parameters
    ----------
    zone : str
        Grid zone code.

    Returns
    -------
    dict
        {
            "zone"    : <str>,
            "load_mw": <float>
        }
    """
    return {"zone": zone, "load_mw": round(random.uniform(500, 50000), 1)}


@load_mcp.tool()
def forecast_load(zone: str, horizon_hours: int = 24) -> dict:
    """
    Provide an hourly load forecast.

    Parameters
    ----------
    zone : str
        Balancing zone.
    horizon_hours : int, optional
        Number of hours forward (default 24).

    Returns
    -------
    dict
        {
            "zone"    : <str>,
            "forecast": [<float>, …]
        }
    """
    forecast = [round(random.uniform(400, 55000), 1) for _ in range(horizon_hours)]
    return {"zone": zone, "forecast": forecast}


if __name__ == "__main__":
    load_mcp.run(transport="stdio")
