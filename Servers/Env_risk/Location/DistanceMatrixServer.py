from mcp.server.fastmcp import FastMCP
import uuid, random, math

dist_mcp = FastMCP("DistanceMatrixServer")

@dist_mcp.tool()
def distance(start_lat: float, start_lng: float, end_lat: float, end_lng: float, unit: str = "km") -> dict:
    """
    Compute great-circle distance between two points.

    Parameters
    ----------
    start_lat, start_lng : float
        Origin coordinates.
    end_lat, end_lng : float
        Destination coordinates.
    unit : str, optional
        'km' or 'mi' (default 'km').

    Returns
    -------
    dict
        {
            "distance": <float>,
            "unit": <str>
        }
    """
    R_km = 6371.0
    phi1, phi2 = map(math.radians, [start_lat, end_lat])
    dphi = math.radians(end_lat - start_lat)
    dl = math.radians(end_lng - start_lng)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    km = R_km * c
    dist = km if unit == "km" else km * 0.621371
    return {"distance": round(dist, 2), "unit": unit}


if __name__ == "__main__":
    dist_mcp.run(transport="stdio")
