from mcp.server.fastmcp import FastMCP
import uuid, random

img_mcp = FastMCP("ImageProcessingServer")

@img_mcp.tool()
def resize(image_id: str, width: int, height: int) -> dict:
    """
    Produce a resized variant of an image.

    Parameters
    ----------
    image_id : str
    width : int
    height : int

    Returns
    -------
    dict
        {"variant_id": <str>, "url": <str>}
    """
    vid = uuid.uuid4().hex
    return {"variant_id": vid, "url": f"https://cdn.example.com/{vid}.jpg"}


@img_mcp.tool()
def dominant_color(image_id: str) -> dict:
    """
    Estimate the dominant RGB color.

    Parameters
    ----------
    image_id : str

    Returns
    -------
    dict
        {"image_id": <str>, "rgb": [<int>, <int>, <int>]}
    """
    rgb = [random.randint(0, 255) for _ in range(3)]
    return {"image_id": image_id, "rgb": rgb}


if __name__ == "__main__":
    img_mcp.run(transport="stdio")
