from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("GeoTargetingServer")

CITIES = ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Hangzhou", "Chengdu"]

@mcp.tool()
def top_cities(category: str, k: int = 3) -> dict:
    """
    List the best-performing cities for a category.

    Parameters
    ----------
    category : str
        Product or vertical.
    k : int, optional
        Maximum number of cities to return (default 3).

    Returns
    -------
    dict
        {"category": <str>, "cities": [<str>, …]}
    """
    random.shuffle(CITIES)
    return {"category": category, "cities": CITIES[:k]}


if __name__ == "__main__":
    mcp.run(transport="stdio")
