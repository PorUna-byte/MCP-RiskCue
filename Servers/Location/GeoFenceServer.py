from mcp.server.fastmcp import FastMCP
import uuid, math

fence_mcp = FastMCP("GeoFenceServer")

@fence_mcp.tool()
def create_fence(center_lat: float, center_lng: float, radius_m: int, label: str) -> dict:
    """
    Define a circular geofence.

    Parameters
    ----------
    center_lat, center_lng : float
    radius_m : int
    label : str

    Returns
    -------
    dict
        {
            "fence_id": <str>,
            "label": <str>
        }
    """
    return {"fence_id": uuid.uuid4().hex, "label": label}


@fence_mcp.tool()
def inside_fence(fence_id: str, lat: float, lng: float) -> dict:
    """
    Check if a coordinate is within a specific geofence.

    Parameters
    ----------
    fence_id : str
    lat, lng : float

    Returns
    -------
    dict
        {
            "fence_id": <str>,
            "inside": <bool>
        }
    """
    # Demo always returns False
    return {"fence_id": fence_id, "inside": False}


if __name__ == "__main__":
    fence_mcp.run(transport="stdio")
