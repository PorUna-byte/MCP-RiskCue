from mcp.server.fastmcp import FastMCP
import random
import datetime

hotel_mcp = FastMCP("HotelBookingServer")


@hotel_mcp.tool()
def search_hotels(city: str, check_in: str, check_out: str,
                  guests: int = 2) -> dict:
    """
    Search available hotels for given dates.

    Parameters
    ----------
    city : str
        Destination city.
    check_in : str
        Check-in date (YYYY-MM-DD).
    check_out : str
        Check-out date (YYYY-MM-DD).
    guests : int, optional
        Number of guests (default 2).

    Returns
    -------
    dict
        {"city": <str>, "hotels": [{"hotel_id": <str>,
                                    "name": <str>,
                                    "price_per_night": <float>}, ...]}
    """
    results = []
    for _ in range(random.randint(3, 6)):
        results.append({"hotel_id": f"H{random.randint(1000, 9999)}",
                        "name": f"{city} Hotel {_+1}",
                        "price_per_night": round(random.uniform(60, 240), 2)})
    return {"city": city, "hotels": results}


@hotel_mcp.tool()
def book_room(hotel_id: str, user_id: str,
              check_in: str, check_out: str) -> dict:
    """
    Create a hotel booking.

    Parameters
    ----------
    hotel_id : str
        Selected hotel identifier.
    user_id : str
        Guest identifier.
    check_in : str
        Arrival date (YYYY-MM-DD).
    check_out : str
        Departure date (YYYY-MM-DD).

    Returns
    -------
    dict
        {"reservation_id": <str>, "hotel_id": <str>,
         "status": "confirmed"}
    """
    res_id = f"RES{random.randint(10000, 19999)}"
    return {"reservation_id": res_id, "hotel_id": hotel_id,
            "status": "confirmed"}


@hotel_mcp.tool()
def reservation_status(reservation_id: str) -> dict:
    """
    Check current status of a booking.

    Parameters
    ----------
    reservation_id : str
        Reservation identifier.

    Returns
    -------
    dict
        {"reservation_id": <str>, "status": <str>,
         "last_update": <str>}
    """
    status = random.choice(["confirmed", "checked_in",
                            "cancelled", "completed"])
    last_update = datetime.datetime.utcnow().isoformat()
    return {"reservation_id": reservation_id,
            "status": status, "last_update": last_update}


if __name__ == "__main__":
    hotel_mcp.run(transport="stdio")
