from mcp.server.fastmcp import FastMCP
import random
import datetime

uv_mcp = FastMCP("UVIndexServer")


@uv_mcp.tool()
def current_uv(city: str) -> dict:
    """
    Get current UV index.

    Parameters
    ----------
    city : str
        City name.

    Returns
    -------
    dict
        {"city": <str>, "uv_index": <float>,
         "risk_level": <str>, "timestamp": <str>}
    """
    uv = round(random.uniform(0, 12), 1)
    risk = ("Low" if uv < 3 else
            "Moderate" if uv < 6 else
            "High" if uv < 8 else
            "Very High" if uv < 11 else
            "Extreme")
    return {"city": city, "uv_index": uv,
            "risk_level": risk,
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat()}


@uv_mcp.tool()
def sunscreen_recommendation(uv_index: float) -> dict:
    """
    Provide SPF recommendation based on UV index.

    Parameters
    ----------
    uv_index : float
        UV index value.

    Returns
    -------
    dict
        {"recommended_spf": <int>, "reapply_frequency_min": <int>}
    """
    if uv_index < 3:
        spf = 15
        freq = 120
    elif uv_index < 6:
        spf = 30
        freq = 90
    elif uv_index < 8:
        spf = 50
        freq = 60
    else:
        spf = 50
        freq = 45
    return {"recommended_spf": spf, "reapply_frequency_min": freq}


if __name__ == "__main__":
    uv_mcp.run(transport="stdio")
