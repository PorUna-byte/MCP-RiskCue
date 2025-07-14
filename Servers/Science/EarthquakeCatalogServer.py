from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

eq_mcp = FastMCP("EarthquakeCatalogServer")

@eq_mcp.tool()
def recent_events(min_mag: float = 5.0, limit: int = 5) -> dict:
    """
    Return a list of recent earthquake events.

    Parameters
    ----------
    min_mag : float, optional
    limit : int, optional

    Returns
    -------
    dict
        {"events": [ {"id": <str>, "mag": <float>, "depth_km": <float>}, … ]}
    """
    events = [{
        "id": uuid.uuid4().hex[:8],
        "mag": round(random.uniform(min_mag, min_mag + 2), 1),
        "depth_km": round(random.uniform(5, 50), 1)
    } for _ in range(limit)]
    return {"events": events}


if __name__ == "__main__":
    eq_mcp.run(transport="stdio")
