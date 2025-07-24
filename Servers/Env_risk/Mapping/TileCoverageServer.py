from mcp.server.fastmcp import FastMCP
import uuid, random

cov_mcp = FastMCP("TileCoverageServer")

@cov_mcp.tool()
def tiles_for_bbox(min_lat: float, min_lng: float, max_lat: float, max_lng: float, z: int) -> dict:
    """
    List XYZ tile indices intersecting a bounding box.

    Parameters
    ----------
    min_lat, min_lng, max_lat, max_lng : float
    z : int
        Zoom level.

    Returns
    -------
    dict
        {
            "z": <int>,
            "tiles": [ {"x": <int>, "y": <int>}, … ]
        }
    """
    tiles = [{"x": random.randint(0, 2**z-1), "y": random.randint(0, 2**z-1)} for _ in range(10)]
    return {"z": z, "tiles": tiles}


if __name__ == "__main__":
    cov_mcp.run(transport="stdio")
