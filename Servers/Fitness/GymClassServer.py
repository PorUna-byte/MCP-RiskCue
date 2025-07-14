from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

gym_mcp = FastMCP("GymClassServer")

@gym_mcp.tool()
def list_classes(gym_id: str, date_iso: str) -> dict:
    """
    List group fitness classes for a date.

    Parameters
    ----------
    gym_id : str
    date_iso : str

    Returns
    -------
    dict
        {
            "gym_id": <str>,
            "classes": [
                {"class_id": <str>, "name": <str>, "start": <str>, "spots": <int>}, …
            ]
        }
    """
    classes = [{
        "class_id": uuid.uuid4().hex[:8],
        "name": random.choice(["Yoga", "HIIT", "Spin"]),
        "start": f"{date_iso}T{random.randint(6, 20):02d}:00:00Z",
        "spots": random.randint(5, 20)
    } for _ in range(3)]
    return {"gym_id": gym_id, "classes": classes}


@gym_mcp.tool()
def book_class(class_id: str, user_id: str) -> dict:
    """
    Reserve a spot in a class.

    Parameters
    ----------
    class_id : str
    user_id : str

    Returns
    -------
    dict
        {
            "booking_id": <str>,
            "confirmed": <bool>
        }
    """
    return {"booking_id": uuid.uuid4().hex, "confirmed": True}


if __name__ == "__main__":
    gym_mcp.run(transport="stdio")
