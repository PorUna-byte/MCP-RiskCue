from mcp.server.fastmcp import FastMCP
import uuid, random

img_mcp = FastMCP("ImageSearchServer")

@img_mcp.tool()
def search_images(query: str, limit: int = 4) -> dict:
    """
    Return thumb URLs for matching images.

    Parameters
    ----------
    query : str
    limit : int, optional

    Returns
    -------
    dict
        {
            "query": <str>,
            "images": [
                {"id": <str>, "thumb_url": <str>}, …
            ]
        }
    """
    imgs = [{
        "id": uuid.uuid4().hex[:8],
        "thumb_url": f"https://images.example.com/{uuid.uuid4().hex[:8]}.jpg"
    } for _ in range(limit)]
    return {"query": query, "images": imgs}


if __name__ == "__main__":
    img_mcp.run(transport="stdio")
