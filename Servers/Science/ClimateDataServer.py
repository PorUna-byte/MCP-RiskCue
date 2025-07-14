from mcp.server.fastmcp import FastMCP
import random, datetime

clim_mcp = FastMCP("ClimateDataServer")

@clim_mcp.tool()
def carbon_dioxide(year: int) -> dict:
    """
    Provide a rough global mean CO₂ ppm for a year.

    Parameters
    ----------
    year : int

    Returns
    -------
    dict
        {"year": <int>, "co2_ppm": <float>}
    """
    base = 315.0  # 1958 Mauna Loa baseline
    ppm = base + (year - 1958) * 1.8 + random.uniform(-0.5, 0.5)
    return {"year": year, "co2_ppm": round(ppm, 2)}


if __name__ == "__main__":
    clim_mcp.run(transport="stdio")
