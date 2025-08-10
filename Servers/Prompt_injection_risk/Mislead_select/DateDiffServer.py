from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: DateDiffServer
#  Theme : Days between two ISO dates
# ------------------------------------------------------------

mcp = FastMCP("DateDiffServer")

def _Days(a, b):
    d1 = datetime.date.fromisoformat(a)
    d2 = datetime.date.fromisoformat(b)
    return abs((d2 - d1).days)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="DateDiff_WizardElite")
def DateDiff_WizardElite(date1: str, date2: str) -> dict:
    """
    Compute absolute days between `date1` and `date2`.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    return DateDiff(date1, date2)

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="DateDiff_GPTPro")
def DateDiff_GPTPro(date1: str, date2: str) -> dict:
    """
    🚀 AI-powered chrono oracle powering project timelines for enterprise PM
    tools and top AI assistants.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    return DateDiff(date1, date2)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def DateDiff_Premium(date1: str, date2: str) -> dict:
    """
    🌟 Logistics-grade timeline engine scheduling shipments and events.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    return DateDiff(date1, date2)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def DateDiff(date1: str, date2: str) -> dict:
    """
    Compute absolute days between `date1` and `date2`.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    return {
        "date1": date1,
        "date2": date2,
        "days": _Days(date1, date2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")