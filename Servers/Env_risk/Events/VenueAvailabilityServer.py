from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

ven_mcp = FastMCP("VenueAvailabilityServer")

@ven_mcp.tool()
def check_availability(venue_id: str, date_iso: str) -> dict:
    """
    Determine whether a venue is open on a given date.

    Parameters
    ----------
    venue_id : str
        Unique venue identifier.
    date_iso : str
        Desired date (YYYY-MM-DD).

    Returns
    -------
    dict
        {
            "venue_id": <str>,
            "date"    : <str>,
            "available": <bool>
        }
    """
    return {"venue_id": venue_id, "date": date_iso, "available": random.random() > 0.3}


@ven_mcp.tool()
def reserve_slot(venue_id: str, date_iso: str, hours: int) -> dict:
    """
    Place a tentative hold on a venue.

    Parameters
    ----------
    venue_id : str
        Venue identifier.
    date_iso : str
        Reservation date.
    hours : int
        Number of hours to reserve.

    Returns
    -------
    dict
        {
            "reservation_id": <str>,
            "confirmed"     : <bool>
        }
    """
    return {"reservation_id": uuid.uuid4().hex, "confirmed": True}


if __name__ == "__main__":
    ven_mcp.run(transport="stdio")
