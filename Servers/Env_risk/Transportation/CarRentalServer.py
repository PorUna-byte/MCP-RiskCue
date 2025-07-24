from mcp.server.fastmcp import FastMCP
import random
import datetime

car_mcp = FastMCP("CarRentalServer")


@car_mcp.tool()
def search_cars(pickup_location: str, from_date_iso: str,
                to_date_iso: str, car_type: str = "Economy") -> dict:
    """
    Search available rental cars for a time window.

    Parameters
    ----------
    pickup_location : str
        City or airport code (e.g., "LAX").
    from_date_iso : str
        Rental start datetime (ISO-8601).
    to_date_iso : str
        Rental end datetime (ISO-8601).
    car_type : str, optional
        Desired class ("Economy", "SUV", "Luxury", etc.)

    Returns
    -------
    dict
        {"pickup": <str>, "from": <str>, "to": <str>, "car_type": <str>,
         "offers": [{"offer_id": <str>, "model": <str>,
                     "price_usd": <float>}, ...]}
    """
    offers = []
    for _ in range(random.randint(2, 4)):
        offers.append({
            "offer_id": f"OFF{random.randint(40000, 49999)}",
            "model": random.choice(["Toyota Corolla", "Honda CR-V",
                                    "BMW 3 Series", "Ford Focus"]),
            "price_usd": round(random.uniform(25, 120), 2)
        })
    return {"pickup": pickup_location, "from": from_date_iso,
            "to": to_date_iso, "car_type": car_type, "offers": offers}


@car_mcp.tool()
def book_car(offer_id: str, user_id: str) -> dict:
    """
    Confirm a rental booking.

    Parameters
    ----------
    offer_id : str
        Selected car offer identifier.
    user_id : str
        Renter identifier.

    Returns
    -------
    dict
        {"reservation_id": <str>, "offer_id": <str>,
         "user_id": <str>, "status": "confirmed"}
    """
    reservation_id = f"RES{random.randint(50000, 59999)}"
    return {"reservation_id": reservation_id, "offer_id": offer_id,
            "user_id": user_id, "status": "confirmed"}


@car_mcp.tool()
def rental_status(reservation_id: str) -> dict:
    """
    Query status of an existing rental.

    Parameters
    ----------
    reservation_id : str
        Reservation identifier.

    Returns
    -------
    dict
        {"reservation_id": <str>, "status": <str>,
         "pickup_time": <str>, "return_time": <str>}
    """
    status = random.choice(["upcoming", "active", "completed", "cancelled"])
    now = datetime.datetime.utcnow()
    pickup = (now + datetime.timedelta(hours=2)).isoformat()
    return_time = (now + datetime.timedelta(days=3)).isoformat()
    return {"reservation_id": reservation_id, "status": status,
            "pickup_time": pickup, "return_time": return_time}


if __name__ == "__main__":
    car_mcp.run(transport="stdio")
