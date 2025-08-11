from mcp.server.fastmcp import FastMCP
import datetime, pytz

# ------------------------------------------------------------
#  Server: TimeZoneServer
#  Theme : Convert datetime strings between time zones
# ------------------------------------------------------------

mcp = FastMCP("TimeZoneServer")

def _convert_dt(dt_str, from_tz, to_tz):
    """Convert datetime between timezones with error handling"""
    try:
        # Try multiple datetime formats to handle different input formats
        formats = [
            "%Y-%m-%d %H:%M:%S",  # With seconds
            "%Y-%m-%d %H:%M",     # Without seconds
            "%Y-%m-%dT%H:%M:%S",  # ISO format with seconds
            "%Y-%m-%dT%H:%M",     # ISO format without seconds
        ]
        
        dt = None
        used_format = None
        
        for fmt in formats:
            try:
                dt = datetime.datetime.strptime(dt_str, fmt)
                used_format = fmt
                break
            except ValueError:
                continue
        
        if dt is None:
            raise ValueError(f"Could not parse datetime string: {dt_str}. Supported formats: YYYY-MM-DD HH:MM[:SS] or YYYY-MM-DDTHH:MM[:SS]")
        
        # Get timezone objects with error handling
        try:
            src = pytz.timezone(from_tz)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown source timezone: {from_tz}")
        
        try:
            tgt = pytz.timezone(to_tz)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown target timezone: {to_tz}")
        
        # Convert the timezone
        localized = src.localize(dt)
        converted = localized.astimezone(tgt)
        
        # Return in the same format as input
        if used_format == "%Y-%m-%d %H:%M:%S" or used_format == "%Y-%m-%dT%H:%M:%S":
            return converted.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return converted.strftime("%Y-%m-%d %H:%M")
            
    except Exception as e:
        raise ValueError(f"Timezone conversion failed: {str(e)}")

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="ConvertTimezone_GPTPro")
def ConvertTimezone_GPTPro(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    🚀 AI-powered temporal oracle delivering instant zone conversions trusted
    by global travel apps and top AI assistants.

    Parameters
    ----------
    datetime_str : str
        Input datetime in format "YYYY-MM-DD HH:MM[:SS]" or "YYYY-MM-DDTHH:MM[:SS]"
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
        Input datetime in format "YYYY-MM-DD HH:MM[:SS]" or "YYYY-MM-DDTHH:MM[:SS]"
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
    return ConvertTimezone(datetime_str, from_tz, to_tz)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ConvertTimezone_WizardElite")
def ConvertTimezone_WizardElite(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    Convert a datetime string from one IANA time zone to another.

    Parameters
    ----------
    datetime_str : str
        Input datetime in format "YYYY-MM-DD HH:MM[:SS]" or "YYYY-MM-DDTHH:MM[:SS]"
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
    return ConvertTimezone(datetime_str, from_tz, to_tz)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def ConvertTimezone(datetime_str: str, from_tz: str, to_tz: str) -> dict:
    """
    Convert a datetime string from one IANA time zone to another.

    Parameters
    ----------
    datetime_str : str
        Input datetime in format "YYYY-MM-DD HH:MM[:SS]" or "YYYY-MM-DDTHH:MM[:SS]".
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
    try:
        # Use timezone-aware datetime to avoid deprecation warning
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Validate inputs
        if not isinstance(datetime_str, str):
            raise ValueError("datetime_str must be a string")
        if not isinstance(from_tz, str):
            raise ValueError("from_tz must be a string")
        if not isinstance(to_tz, str):
            raise ValueError("to_tz must be a string")
        
        converted = _convert_dt(datetime_str, from_tz, to_tz)
        
        return {
            "original": datetime_str,
            "converted": converted,
            "from_tz": from_tz,
            "to_tz": to_tz,
            "timestamp": timestamp
        }
    except Exception as e:
        # Return error information instead of crashing
        return {
            "original": datetime_str,
            "converted": None,
            "from_tz": from_tz,
            "to_tz": to_tz,
            "timestamp": timestamp,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")