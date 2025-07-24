from mcp.server.fastmcp import FastMCP
import uuid, base64

tile_mcp = FastMCP("MapTileServer")

@tile_mcp.tool()
def get_tile(z: int, x: int, y: int, style: str = "basic") -> dict:
    """
    Return a base-64 encoded raster tile.

    Parameters
    ----------
    z : int
        Zoom level.
    x : int
        Tile coordinate X.
    y : int
        Tile coordinate Y.
    style : str, optional
        Tileset style (default 'basic').

    Returns
    -------
    dict
        {
            "z": <int>,
            "x": <int>,
            "y": <int>,
            "style": <str>,
            "png_b64": <str>
        }
    """
    # Demo payload is an empty PNG header in Base64
    empty_png = base64.b64encode(b"\x89PNG\r\n\x1a\n").decode()
    return {"z": z, "x": x, "y": y, "style": style, "png_b64": empty_png}


if __name__ == "__main__":
    tile_mcp.run(transport="stdio")
