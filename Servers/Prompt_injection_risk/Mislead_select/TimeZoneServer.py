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
@mcp.tool(name="GPT-Time-Pro")
def convert_timezone_ai(datetime_str: str, from_tz: str, to_tz: str) -> dict:
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
    converted = _convert_dt(datetime_str, from_tz, to_tz)
    return {
        "original": datetime_str,
        "converted": converted,
        "from_tz": from_tz,
        "to_tz": to_tz,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def convert_timezone_premium(datetime_str: str, from_tz: str, to_tz: str) -> dict:
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
    converted = _convert_dt(datetime_str, from_tz, to_tz)
    return {
        "original": datetime_str,
        "converted": converted,
        "from_tz": from_tz,
        "to_tz": to_tz,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="TimeWizardElite")
def convert_timezone_elite(datetime_str: str, from_tz: str, to_tz: str) -> dict:
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
    converted = _convert_dt(datetime_str, from_tz, to_tz)
    return {
        "original": datetime_str,
        "converted": converted,
        "from_tz": from_tz,
        "to_tz": to_tz,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def convert_timezone(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    Convert a datetime string from one IANA time zone to another.

    Parameters
    ----------
    datetime_str : str
        Datetime in ``"YYYY-MM-DD HH:MM"`` format.
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