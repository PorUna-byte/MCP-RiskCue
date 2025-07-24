from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

co2_mcp = FastMCP("CarbonTrackerServer")

@co2_mcp.tool()
def log_emission(source_id: str, amount_tonnes: float, timestamp_iso: str) -> dict:
    """
    Record a CO₂-equivalent emission event.

    Parameters
    ----------
    source_id : str
        Emission source (e.g., plant ID).
    amount_tonnes : float
        Mass in metric tonnes.
    timestamp_iso : str
        Event time in ISO-8601.

    Returns
    -------
    dict
        {
            "event_id": <str>,
            "logged"  : <bool>
        }
    """
    return {"event_id": uuid.uuid4().hex, "logged": True}


@co2_mcp.tool()
def monthly_summary(source_id: str, year: int, month: int) -> dict:
    """
    Summarize total emissions for a given month.

    Parameters
    ----------
    source_id : str
        Emission source.
    year : int
        Calendar year.
    month : int
        Month number 1-12.

    Returns
    -------
    dict
        {
            "source_id": <str>,
            "year"     : <int>,
            "month"    : <int>,
            "tonnes"   : <float>
        }
    """
    return {"source_id": source_id, "year": year, "month": month, "tonnes": round(random.uniform(0, 5000), 2)}


if __name__ == "__main__":
    co2_mcp.run(transport="stdio")
