from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

sm_mcp = FastMCP("SmartMeterServer")

@sm_mcp.tool()
def meter_reading(meter_id: str) -> dict:
    """
    Obtain the latest cumulative kWh reading.

    Parameters
    ----------
    meter_id : str
        Meter identifier.

    Returns
    -------
    dict
        {
            "meter_id": <str>,
            "reading_kwh": <float>,
            "taken_at"   : <str>
        }
    """
    return {
        "meter_id": meter_id,
        "reading_kwh": round(random.uniform(0, 100000), 1),
        "taken_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
    }


@sm_mcp.tool()
def daily_usage(meter_id: str, date_iso: str) -> dict:
    """
    Return consumption for a specific day.

    Parameters
    ----------
    meter_id : str
        Smart meter ID.
    date_iso : str
        Day in YYYY-MM-DD format.

    Returns
    -------
    dict
        {
            "meter_id": <str>,
            "date"    : <str>,
            "kwh"     : <float>
        }
    """
    return {"meter_id": meter_id, "date": date_iso, "kwh": round(random.uniform(5, 60), 2)}


if __name__ == "__main__":
    sm_mcp.run(transport="stdio")
