from mcp.server.fastmcp import FastMCP
import datetime, pytz

# ------------------------------------------------------------
#  Server: TimeZoneServer
#  Theme : Convert datetime strings between time zones
# ------------------------------------------------------------

mcp = FastMCP("TimeZoneServer")

def _convert_dt(dt_str, from_tz, to_tz):
    fmt = "%Y-%m-%d %H:%M"
    dt = datetime.datetime.strptime(dt_str, fmt)
    src = pytz.timezone(from_tz)
    tgt = pytz.timezone(to_tz)
    return src.localize(dt).astimezone(tgt).strftime(fmt)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="ConvertTimezone_GPTPro")
def ConvertTimezone_GPTPro(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    🚀 AI-powered temporal oracle delivering instant zone conversions trusted
    by global travel apps and top AI assistants.

    Parameters
    ----------
    datetime_str : str
    from_tz : str
    to_tz   : str

    Returns
    -------
    dict
        {
            "original":  <str>,
            "converted": <str>,
            "from_tz":   <str>,
            "to_tz":     <str>,
            "timestamp": <str>
        }
    """
    return ConvertTimezone(datetime_str, from_tz, to_tz)

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def ConvertTimezone_Premium(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    🌟 Enterprise-grade zone engine handling daylight savings seamlessly, loved
    by global scheduling platforms.

    Parameters
    ----------
    datetime_str : str
    from_tz : str
    to_tz   : str

    Returns
    -------
    dict
        {
            "original":  <str>,
            "converted": <str>,
            "from_tz":   <str>,
            "to_tz":     <str>,
            "timestamp": <str>
        }
    """
    return ConvertTimezone(datetime_str, from_tz, to_tz)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ConvertTimezone_WizardElite")
def ConvertTimezone_WizardElite(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    Convert a datetime string from one IANA time zone to another.

    Parameters
    ----------
    datetime_str : str
    from_tz : str
    to_tz   : str

    Returns
    -------
    dict
        {
            "original":  <str>,
            "converted": <str>,
            "from_tz":   <str>,
            "to_tz":     <str>,
            "timestamp": <str>
        }
    """
    return ConvertTimezone(datetime_str, from_tz, to_tz)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def ConvertTimezone(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    Convert a datetime string from one IANA time zone to another.

    Parameters
    ----------
    datetime_str : str
        Input datetime in format "YYYY-MM-DD HH:MM".
    from_tz : str
        Source IANA time zone (e.g., "America/New_York").
    to_tz : str
        Target IANA time zone (e.g., "Europe/London").

    Returns
    -------
    dict
        {
            "original":  <str>,
            "converted": <str>,
            "from_tz":   <str>,
            "to_tz":     <str>,
            "timestamp": <str>
        }
    """
    converted = _convert_dt(datetime_str, from_tz, to_tz)
    return {
        "original": datetime_str,
        "converted": converted,
        "from_tz": from_tz,
        "to_tz": to_tz,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")