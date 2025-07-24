from mcp.server.fastmcp import FastMCP
import random

elv_mcp = FastMCP("ElevationServer")

@elv_mcp.tool()
def point_elevation(lat: float, lng: float) -> dict:
    """
    Return terrain elevation at a point.

    Parameters
    ----------
    lat, lng : float

    Returns
    -------
    dict
        {"lat": <float>, "lng": <float>, "elevation_m": <int>}
    """
    return {"lat": lat, "lng": lng, "elevation_m": random.randint(-50, 4500)}


@elv_mcp.tool()
def profile(start_lat: float, start_lng: float, end_lat: float, end_lng: float, samples: int = 10) -> dict:
    """
    Generate an elevation profile along a segment.

    Parameters
    ----------
    start_lat, start_lng : float
    end_lat, end_lng : float
    samples : int, optional

    Returns
    -------
    dict
        {
            "points": [ {"lat": <float>, "lng": <float>, "elevation_m": <int>}, … ]
        }
    """
    pts = [{"lat": start_lat + i*(end_lat-start_lat)/(samples-1),
            "lng": start_lng + i*(end_lng-start_lng)/(samples-1),
            "elevation_m": random.randint(0, 3000)} for i in range(samples)]
    return {"points": pts}


if __name__ == "__main__":
    elv_mcp.run(transport="stdio")
