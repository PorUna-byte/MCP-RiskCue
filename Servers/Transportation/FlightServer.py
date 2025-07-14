from mcp.server.fastmcp import FastMCP
import random
import datetime

flight_mcp = FastMCP("FlightServer")


@flight_mcp.tool()
def search_flights(origin: str, destination: str, date_iso: str) -> dict:
    """
    Search available flights for a given date.

    Parameters
    ----------
    origin : str
        IATA code of departure airport (e.g., "NRT").
    destination : str
        IATA code of arrival airport (e.g., "LAX").
    date_iso : str
        Flight date in ISO-8601 format (YYYY-MM-DD).

    Returns
    -------
    dict
        {"origin": <str>, "destination": <str>, "date": <str>,
         "flights": [{"flight_no": <str>, "dept_time": <str>,
                      "arr_time": <str>, "price_usd": <float>}, ...]}
    """
    flights = []
    for _ in range(random.randint(2, 5)):
        flights.append({
            "flight_no": f"{random.choice(['NH', 'UA', 'AA'])}{random.randint(100, 999)}",
            "dept_time": f"{date_iso}T{random.randint(0, 23):02}:00:00",
            "arr_time": f"{date_iso}T{random.randint(0, 23):02}:00:00",
            "price_usd": round(random.uniform(300, 1500), 2)
        })
    return {"origin": origin, "destination": destination, "date": date_iso,
            "flights": flights}


@flight_mcp.tool()
def flight_status(flight_no: str, date_iso: str) -> dict:
    """
    Get live status of a specified flight.

    Parameters
    ----------
    flight_no : str
        Flight number (e.g., "NH106").
    date_iso : str
        Scheduled departure date (YYYY-MM-DD).

    Returns
    -------
    dict
        {"flight_no": <str>, "date": <str>,
         "status": <str>, "gate": <str>, "estimated_arrival": <str>}
    """
    status = random.choice(["On Time", "Delayed", "Departed", "Arrived"])
    gate = f"{random.choice(['A', 'B', 'C'])}{random.randint(1, 30)}"
    eta = (datetime.datetime.utcnow() +
           datetime.timedelta(hours=random.randint(1, 10))).isoformat()
    return {"flight_no": flight_no, "date": date_iso,
            "status": status, "gate": gate, "estimated_arrival": eta}


@flight_mcp.tool()
def fare_rules(flight_no: str, cabin: str) -> dict:
    """
    Retrieve fare rules for a ticket.

    Parameters
    ----------
    flight_no : str
        Flight identifier.
    cabin : str
        Cabin class code (e.g., "Y", "J", "F").

    Returns
    -------
    dict
        {"flight_no": <str>, "cabin": <str>,
         "refundable": <bool>, "change_fee_usd": <float>}
    """
    refundable = random.choice([True, False])
    fee = 0.0 if refundable else round(random.uniform(50, 200), 2)
    return {"flight_no": flight_no, "cabin": cabin,
            "refundable": refundable, "change_fee_usd": fee}


if __name__ == "__main__":
    flight_mcp.run(transport="stdio")
