from mcp.server.fastmcp import FastMCP
import random
import datetime

train_mcp = FastMCP("TrainServer")


@train_mcp.tool()
def search_trains(origin_station: str, dest_station: str, date_iso: str) -> dict:
    """
    List train services between two stations.

    Parameters
    ----------
    origin_station : str
        Origin station code (e.g., "TKY").
    dest_station : str
        Destination station code (e.g., "OSA").
    date_iso : str
        Travel date (YYYY-MM-DD).

    Returns
    -------
    dict
        {"origin": <str>, "destination": <str>, "date": <str>,
         "services": [{"train_no": <str>, "dept": <str>,
                       "arr": <str>, "seat_available": <int>}, ...]}
    """
    services = []
    for _ in range(random.randint(3, 6)):
        services.append({
            "train_no": f"{random.choice(['Hikari', 'Nozomi', 'Kodama'])}{random.randint(100,999)}",
            "dept": f"{date_iso}T{random.randint(6, 20):02}:00:00",
            "arr": f"{date_iso}T{random.randint(8, 23):02}:00:00",
            "seat_available": random.randint(0, 200)
        })
    return {"origin": origin_station, "destination": dest_station,
            "date": date_iso, "services": services}


@train_mcp.tool()
def train_status(train_no: str, date_iso: str) -> dict:
    """
    Check running status of a train.

    Parameters
    ----------
    train_no : str
        Train identifier (e.g., "Nozomi123").
    date_iso : str
        Scheduled departure date.

    Returns
    -------
    dict
        {"train_no": <str>, "date": <str>,
         "status": <str>, "delay_min": <int>}
    """
    status = random.choice(["On Schedule", "Delayed", "Departed", "Arrived"])
    delay = 0 if status != "Delayed" else random.randint(5, 60)
    return {"train_no": train_no, "date": date_iso,
            "status": status, "delay_min": delay}


if __name__ == "__main__":
    train_mcp.run(transport="stdio")
