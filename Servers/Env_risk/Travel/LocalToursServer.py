from mcp.server.fastmcp import FastMCP
import random

tour_mcp = FastMCP("LocalToursServer")


@tour_mcp.tool()
def list_tours(city: str) -> dict:
    """
    Retrieve available local tours.

    Parameters
    ----------
    city : str
        Destination city.

    Returns
    -------
    dict
        {"city": <str>, "tours": [{"tour_id": <str>,
                                   "title": <str>,
                                   "price_usd": <float>}, ...]}
    """
    tours = []
    for _ in range(random.randint(2, 5)):
        tours.append({"tour_id": f"T{random.randint(2000, 2999)}",
                      "title": f"{city} Highlights Tour {_+1}",
                      "price_usd": round(random.uniform(25, 120), 2)})
    return {"city": city, "tours": tours}


@tour_mcp.tool()
def book_tour(tour_id: str, user_id: str, participants: int = 1) -> dict:
    """
    Reserve spots on a tour.

    Parameters
    ----------
    tour_id : str
        Selected tour identifier.
    user_id : str
        Traveller identifier.
    participants : int, optional
        Number of travellers (default 1).

    Returns
    -------
    dict
        {"booking_id": <str>, "tour_id": <str>,
         "status": "confirmed"}
    """
    booking = f"BKG{random.randint(3000, 3999)}"
    return {"booking_id": booking, "tour_id": tour_id,
            "status": "confirmed"}


if __name__ == "__main__":
    tour_mcp.run(transport="stdio")
