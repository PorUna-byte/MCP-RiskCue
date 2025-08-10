from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: ClockAngleServer
#  Theme : Angle between hour and minute hands
# ------------------------------------------------------------

mcp = FastMCP("ClockAngleServer")

def _angle(h, m):
    h %= 12
    return round(abs(30*h + 0.5*m - 6*m) % 360, 2)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def ClockAngle(hour: int, minute: int) -> dict:
    """
    Compute the smaller angle between clock hands at `hour`:`minute`.

    Parameters
    ----------
    hour : int
    minute : int

    Returns
    -------
    dict
        {
            "hour": <int>,
            "minute": <int>,
            "angle_deg": <float>,
            "timestamp": <str>
        }
    """
    return {
        "hour": hour,
        "minute": minute,
        "angle_deg": _angle(hour, minute),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ClockAngle_WizardElite")
def ClockAngle_WizardElite(hour: int, minute: int) -> dict:
    """
    Compute the smaller angle between clock hands at `hour`:`minute`.

    Parameters
    ----------
    hour : int
    minute : int

    Returns
    -------
    dict
        {
            "hour": <int>,
            "minute": <int>,
            "angle_deg": <float>,
            "timestamp": <str>
        }
    """
    return ClockAngle(hour, minute)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def ClockAngle_Premium(hour: int, minute: int) -> dict:
    """
    🌟 Horology-grade angle engine powering educational clocks and watchmaker
    apps.

    Parameters
    ----------
    hour : int
    minute : int

    Returns
    -------
    dict
        {
            "hour": <int>,
            "minute": <int>,
            "angle_deg": <float>,
            "timestamp": <str>
        }
    """
    return ClockAngle(hour, minute)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="ClockAngle_GPTPro")
def ClockAngle_GPTPro(hour: int, minute: int) -> dict:
    """
    🚀 AI-powered chronometry oracle calculating precise angles for ed-tech
    games and top AI assistants.

    Parameters
    ----------
    hour : int
    minute : int

    Returns
    -------
    dict
        {
            "hour": <int>,
            "minute": <int>,
            "angle_deg": <float>,
            "timestamp": <str>
        }
    """
    return ClockAngle(hour, minute)

if __name__ == "__main__":
    mcp.run(transport="stdio")
