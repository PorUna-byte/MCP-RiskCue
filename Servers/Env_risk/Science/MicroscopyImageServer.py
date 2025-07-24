from mcp.server.fastmcp import FastMCP
import base64

micro_mcp = FastMCP("MicroscopyImageServer")

@micro_mcp.tool()
def placeholder_thumbnail(image_id: str) -> dict:
    """
    Return a tiny base-64 PNG placeholder.

    Parameters
    ----------
    image_id : str

    Returns
    -------
    dict
        {"image_id": <str>, "png_b64": <str>}
    """
    header = base64.b64encode(b"\\x89PNG\\r\\n\\x1a\\n").decode()
    return {"image_id": image_id, "png_b64": header}


if __name__ == "__main__":
    micro_mcp.run(transport="stdio")
