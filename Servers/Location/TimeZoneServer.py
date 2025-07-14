from mcp.server.fastmcp import FastMCP
import random, datetime

tz_mcp = FastMCP("TimeZoneServer")

@tz_mcp.tool()
def time_zone(lat: float, lng: float) -> dict:
    """
    Return the IANA time zone ID and current local time.

    Parameters
    ----------
    lat, lng : float

    Returns
    -------
    dict
        {
            "tz_id": <str>,
            "local_time": <str>
        }
    """
    zones = ["America/New_York", "Europe/Paris", "Asia/Tokyo", "Australia/Sydney"]
    tz = random.choice(zones)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {"tz_id": tz, "local_time": now}


if __name__ == "__main__":
    tz_mcp.run(transport="stdio")
