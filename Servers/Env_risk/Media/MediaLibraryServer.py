from mcp.server.fastmcp import FastMCP
import uuid, random

lib_mcp = FastMCP("MediaLibraryServer")

@lib_mcp.tool()
def add_asset(title: str, media_type: str, duration_sec: int) -> dict:
    """
    Register a new media asset in the library.

    Parameters
    ----------
    title : str
        Human-readable title.
    media_type : str
        'video', 'audio', or 'image'.
    duration_sec : int
        Length in seconds (use 0 for images).

    Returns
    -------
    dict
        {"asset_id": <str>, "title": <str>}
    """
    return {"asset_id": uuid.uuid4().hex, "title": title}


@lib_mcp.tool()
def search_assets(keyword: str, limit: int = 5) -> dict:
    """
    Simple title substring search.

    Parameters
    ----------
    keyword : str
    limit : int, optional

    Returns
    -------
    dict
        {"matches": [ {"asset_id": <str>, "title": <str>}, … ]}
    """
    matches = [{"asset_id": uuid.uuid4().hex[:8], "title": f"{keyword.title()} Clip {i}"} for i in range(limit)]
    return {"matches": matches}


if __name__ == "__main__":
    lib_mcp.run(transport="stdio")
