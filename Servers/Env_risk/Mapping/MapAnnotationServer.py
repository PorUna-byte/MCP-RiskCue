from mcp.server.fastmcp import FastMCP
import uuid, datetime

ann_mcp = FastMCP("MapAnnotationServer")

@ann_mcp.tool()
def add_marker(lat: float, lng: float, label: str) -> dict:
    """
    Add a labeled marker to the map.

    Parameters
    ----------
    lat, lng : float
    label : str

    Returns
    -------
    dict
        {"marker_id": <str>, "created_at": <str>}
    """
    return {"marker_id": uuid.uuid4().hex, "created_at": datetime.datetime.utcnow().isoformat() + "Z"}


@ann_mcp.tool()
def delete_marker(marker_id: str) -> dict:
    """
    Remove an existing marker.

    Parameters
    ----------
    marker_id : str

    Returns
    -------
    dict
        {"marker_id": <str>, "deleted": <bool>}
    """
    return {"marker_id": marker_id, "deleted": True}


if __name__ == "__main__":
    ann_mcp.run(transport="stdio")
