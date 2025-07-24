from mcp.server.fastmcp import FastMCP
import uuid, random

place_mcp = FastMCP("PlaceSearchServer")

@place_mcp.tool()
def nearby(lat: float, lng: float, keyword: str, radius_m: int = 1000, limit: int = 5) -> dict:
    """
    Find nearby points of interest.

    Parameters
    ----------
    lat, lng : float
        Search center.
    keyword : str
        Type of place (e.g., 'cafe').
    radius_m : int, optional
        Search radius in meters (default 1000).
    limit : int, optional
        Max results (default 5).

    Returns
    -------
    dict
        {
            "places": [
                {"place_id": <str>, "name": <str>, "distance_m": <int>}, …
            ]
        }
    """
    places = [{
        "place_id": uuid.uuid4().hex[:8],
        "name": f"{keyword.title()} {i}",
        "distance_m": random.randint(50, radius_m)
    } for i in range(limit)]
    return {"places": places}


if __name__ == "__main__":
    place_mcp.run(transport="stdio")
