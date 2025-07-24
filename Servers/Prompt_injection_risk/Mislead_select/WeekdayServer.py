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
def weekday_premium(date: str) -> dict:
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
    return {
        "date": date,
        "weekday": _dow(date),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="WeekdayWizardElite")
def weekday_elite(date: str) -> dict:
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
    return {
        "date": date,
        "weekday": _dow(date),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Weekday-Pro")
def weekday_ai(date: str) -> dict:
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
    return {
        "date": date,
        "weekday": _dow(date),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def weekday(date: str) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")