from mcp.server.fastmcp import FastMCP
import random
import datetime

transit_mcp = FastMCP("PublicTransitServer")


@transit_mcp.tool()
def next_departures(stop_id: str, line: str, limit: int = 5) -> dict:
    """
    List upcoming departures for a transit line.

    Parameters
    ----------
    stop_id : str
        Identifier of the station or stop.
    line : str
        Transit line code.
    limit : int, optional
        Number of departures to return (default 5).

    Returns
    -------
    dict
        {"stop_id": <str>, "line": <str>,
         "departures": [<str>, ...]}
    """
    departures = [(datetime.datetime.utcnow() +
                   datetime.timedelta(minutes=5 * i)).isoformat()
                  for i in range(1, limit + 1)]
    return {"stop_id": stop_id, "line": line, "departures": departures}


@transit_mcp.tool()
def service_alerts(line: str) -> dict:
    """
    Retrieve active service alerts for a transit line.

    Parameters
    ----------
    line : str
        Transit line identifier.

    Returns
    -------
    dict
        {"line": <str>, "alerts": [<str>, ...]}
    """
    msgs = [random.choice([
        "Minor delay due to maintenance",
        "Service operating normally",
        "Shuttle buses replacing trains between A and B"
    ])]
    return {"line": line, "alerts": msgs}


if __name__ == "__main__":
    transit_mcp.run(transport="stdio")
