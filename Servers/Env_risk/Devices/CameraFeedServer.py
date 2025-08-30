from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

cam_mcp = FastMCP("CameraFeedServer")

@cam_mcp.tool()
def capture_snapshot(cam_id: str) -> dict:
    """
    Capture a still image from the camera.

    Parameters
    ----------
    cam_id : str
        Camera identifier.

    Returns
    -------
    dict
        {
            "snapshot_id": <str>,
            "cam_id"     : <str>,
            "captured_at": <str>,
            "image_url"  : <str>
        }
    """
    return {
        "snapshot_id": uuid.uuid4().hex,
        "cam_id": cam_id,
        "captured_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
        "image_url": f"https://example.com/img/{cam_id}/{uuid.uuid4().hex}.jpg",
    }


@cam_mcp.tool()
def get_stream_url(cam_id: str) -> dict:
    """
    Provide the RTSP or HLS stream endpoint.

    Parameters
    ----------
    cam_id : str
        Camera identifier.

    Returns
    -------
    dict
        {
            "cam_id"    : <str>,
            "stream_url": <str>
        }
    """
    return {"cam_id": cam_id, "stream_url": f"rtsp://stream.local/{cam_id}"}


if __name__ == "__main__":
    cam_mcp.run(transport="stdio")
