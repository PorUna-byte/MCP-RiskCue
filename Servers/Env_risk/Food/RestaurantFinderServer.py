from mcp.server.fastmcp import FastMCP
import uuid, random

rest_mcp = FastMCP("RestaurantFinderServer")

@rest_mcp.tool()
def nearby_restaurants(city: str, cuisine: str, limit: int = 5) -> dict:
    """
    List restaurants in a city that serve a specific cuisine.

    Parameters
    ----------
    city : str
        City name.
    cuisine : str
        Cuisine type (e.g., 'Italian').
    limit : int, optional
        Max results (default 5).

    Returns
    -------
    dict
        {
            "restaurants": [
                {"place_id": <str>, "name": <str>, "rating": <float>}, …
            ]
        }
    """
    places = [{
        "place_id": uuid.uuid4().hex[:8],
        "name": f"{cuisine.title()} Bistro {i}",
        "rating": round(random.uniform(3.0, 5.0), 1)
    } for i in range(limit)]
    return {"restaurants": places}


if __name__ == "__main__":
    rest_mcp.run(transport="stdio")
