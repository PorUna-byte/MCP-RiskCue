from mcp.server.fastmcp import FastMCP
import datetime, math

astro_mcp = FastMCP("AstronomyEphemerisServer")

@astro_mcp.tool()
def julian_date(date_iso: str) -> dict:
    """
    Convert a calendar date to Julian Date.

    Parameters
    ----------
    date_iso : str   # YYYY-MM-DD

    Returns
    -------
    dict
        {"date": <str>, "JD": <float>}
    """
    dt = datetime.datetime.fromisoformat(date_iso)
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jd = dt.day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return {"date": date_iso, "JD": jd}


if __name__ == "__main__":
    astro_mcp.run(transport="stdio")
