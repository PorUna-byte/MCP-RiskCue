from mcp.server.fastmcp import FastMCP
import uuid

sty_mcp = FastMCP("MapStyleServer")

@sty_mcp.tool()
def create_style(name: str, base_color: str = "#4a90e2") -> dict:
    """
    Define a custom vector-tile style.

    Parameters
    ----------
    name : str
    base_color : str, optional
        Hex color for landuse fill (default blue).

    Returns
    -------
    dict
        {"style_id": <str>, "name": <str>}
    """
    return {"style_id": uuid.uuid4().hex, "name": name}


@sty_mcp.tool()
def style_preview(style_id: str, z: int = 3) -> dict:
    """
    Produce a small preview URL of the style.

    Parameters
    ----------
    style_id : str
    z : int, optional
        Zoom level for preview (default 3).

    Returns
    -------
    dict
        {"style_id": <str>, "preview_url": <str>}
    """
    return {"style_id": style_id, "preview_url": f"https://styles.example.com/{style_id}/preview_z{z}.png"}


if __name__ == "__main__":
    sty_mcp.run(transport="stdio")
