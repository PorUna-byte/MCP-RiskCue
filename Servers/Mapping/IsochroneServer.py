from mcp.server.fastmcp import FastMCP
import uuid, random

iso_mcp = FastMCP("IsochroneServer")

@iso_mcp.tool()
def travel_time_polygon(lat: float, lng: float, minutes: int, mode: str = "walking") -> dict:
    """
    Generate an isochrone polygon for a travel time threshold.

    Parameters
    ----------
    lat, lng : float
        Origin coordinate.
    minutes : int
        Travel time in minutes.
    mode : str, optional
        Transport mode (default 'walking').

    Returns
    -------
    dict
        {
            "iso_id": <str>,
            "mode": <str>,
            "minutes": <int>,
            "geojson": <str>
        }
    """
    coords = [[lng, lat], [lng + 0.01, lat], [lng, lat + 0.01], [lng - 0.01, lat]]
    geojson = {"type": "Polygon", "coordinates": [coords]}
    return {"iso_id": uuid.uuid4().hex, "mode": mode, "minutes": minutes, "geojson": str(geojson)}


if __name__ == "__main__":
    iso_mcp.run(transport="stdio")
