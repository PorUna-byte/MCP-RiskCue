from mcp.server.fastmcp import FastMCP
import math

proj_mcp = FastMCP("ProjectionServer")

@proj_mcp.tool()
def wgs84_to_web_mercator(lat: float, lng: float) -> dict:
    """
    Convert geographic WGS-84 to Web Mercator (EPSG:3857).

    Parameters
    ----------
    lat : float
        Latitude in decimal degrees.
    lng : float
        Longitude in decimal degrees.

    Returns
    -------
    dict
        {
            "x": <float>,   # meters
            "y": <float>
        }
    """
    origin_shift = 20037508.34
    x = lng * origin_shift / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) * origin_shift / math.pi
    return {"x": round(x, 2), "y": round(y, 2)}


if __name__ == "__main__":
    proj_mcp.run(transport="stdio")
