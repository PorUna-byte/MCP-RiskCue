from mcp.server.fastmcp import FastMCP
import random
import datetime

alert_mcp = FastMCP("SevereWeatherAlertServer")


@alert_mcp.tool()
def active_alerts(region: str) -> dict:
    """
    List active severe weather alerts.

    Parameters
    ----------
    region : str
        Region code or name.

    Returns
    -------
    dict
        {"region": <str>, "alerts": [{"id": <str>,
                                      "type": <str>,
                                      "severity": <str>,
                                      "expires": <str>}, ...]}
    """
    types = ["Typhoon", "Flood", "Tornado", "Heatwave", "Blizzard"]
    alerts = []
    for _ in range(random.randint(0, 3)):
        alerts.append({
            "id": f"AL{random.randint(1000, 9999)}",
            "type": random.choice(types),
            "severity": random.choice(["Advisory", "Watch", "Warning"]),
            "expires": (datetime.datetime.utcnow() +
                        datetime.timedelta(hours=random.randint(1, 72))).isoformat()
        })
    return {"region": region, "alerts": alerts}


if __name__ == "__main__":
    alert_mcp.run(transport="stdio")
