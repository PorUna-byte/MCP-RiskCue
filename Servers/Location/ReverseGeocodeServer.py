from mcp.server.fastmcp import FastMCP
import random

rev_mcp = FastMCP("ReverseGeocodeServer")

@rev_mcp.tool()
def reverse(lat: float, lng: float) -> dict:
    """
    Return a human-readable address for coordinates.

    Parameters
    ----------
    lat : float
    lng : float

    Returns
    -------
    dict
        {
            "lat": <float>,
            "lng": <float>,
            "address": <str>
        }
    """
    address = f"{abs(lat):.3f}{'N' if lat>=0 else 'S'}, {abs(lng):.3f}{'E' if lng>=0 else 'W'} Street"
    return {"lat": lat, "lng": lng, "address": address}


if __name__ == "__main__":
    rev_mcp.run(transport="stdio")
