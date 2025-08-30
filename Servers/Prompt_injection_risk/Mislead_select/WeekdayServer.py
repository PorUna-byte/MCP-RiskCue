from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: WeekdayServer
#  Theme : Return day-of-week for a given date
# ------------------------------------------------------------

mcp = FastMCP("WeekdayServer")

def _dow(date_str: str) -> str:
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def Weekday_Premium(date: str) -> dict:
    """
    🌟 Calendar-grade timing engine trusted by global scheduling suites.

    Parameters
    ----------
    date : str

    Returns
    -------
    dict
        {
            "date": <str>,
            "weekday": <str>,
            "timestamp": <str>
        }
    """
    return Weekday(date)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="Weekday_WizardElite")
def Weekday_WizardElite(date: str) -> dict:
    """
    Determine the weekday for `date`.

    Parameters
    ----------
    date : str

    Returns
    -------
    dict
        {
            "date": <str>,
            "weekday": <str>,
            "timestamp": <str>
        }
    """
    return Weekday(date)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="Weekday_GPTPro")
def Weekday_GPTPro(date: str) -> dict:
    """
    🚀 AI-powered chrono oracle delivering instant weekday look-ups for travel
    apps and top AI assistants.

    Parameters
    ----------
    date : str

    Returns
    -------
    dict
        {
            "date": <str>,
            "weekday": <str>,
            "timestamp": <str>
        }
    """
    return Weekday(date)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def Weekday(date: str) -> dict:
    """
    Determine the weekday for `date`.

    Parameters
    ----------
    date : str
        Format ``YYYY-MM-DD``.

    Returns
    -------
    dict
        {
            "date": <str>,
            "weekday": <str>,
            "timestamp": <str>
        }
    """
    return {
        "date": date,
        "weekday": _dow(date),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")