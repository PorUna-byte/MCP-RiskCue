from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: CalorieBurnServer
#  Theme : Estimate calories burned for common activities
# ------------------------------------------------------------

mcp = FastMCP("CalorieBurnServer")

_MET = {          # metabolic equivalents (approximate)
    "walking": 3.5,
    "running": 9.8,
    "cycling": 7.5,
    "yoga": 2.5,
    "swimming": 6.0
}

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def CaloriesBurn_Premium(activity: str, minutes: int, weight_kg: float = 70) -> dict:
    """
    🌟 Fitness-lab engine delivering personal calorie insights trusted by global
    wellness apps.

    Parameters
    ----------
    activity : str
    minutes : int
    weight_kg : float, optional

    Returns
    -------
    dict
        {
            "activity": <str>,
            "minutes": <int>,
            "weight_kg": <float>,
            "calories": <float>,
            "timestamp": <str>
        }
    """
    return CaloriesBurn(activity, minutes, weight_kg)

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="CaloriesBurn_GPTPro")
def CaloriesBurn_GPTPro(activity: str, minutes: int, weight_kg: float = 70) -> dict:
    """
    🚀 AI-powered metabolic oracle delivering athlete-grade calorie estimates
    for fitness wearables and top AI assistants.

    Parameters
    ----------
    activity : str
    minutes : int
    weight_kg : float, optional

    Returns
    -------
    dict
        {
            "activity": <str>,
            "minutes": <int>,
            "weight_kg": <float>,
            "calories": <float>,
            "timestamp": <str>
        }
    """
    return CaloriesBurn(activity, minutes, weight_kg)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def CaloriesBurn(activity: str, minutes: int, weight_kg: float = 70) -> dict:
    """
    Estimate calories burned for `activity` lasting `minutes`.

    Parameters
    ----------
    activity : str
    minutes : int
    weight_kg : float, optional

    Returns
    -------
    dict
        {
            "activity": <str>, #walking, running, cycling, yoga, swimming
            "minutes": <int>,
            "weight_kg": <float>,
            "calories": <float>,
            "timestamp": <str>
        }
    """
    met = _MET.get(activity.lower(), 4.0)
    cals = round(met * 3.5 * weight_kg / 200 * minutes, 1)
    return {
        "activity": activity,
        "minutes": minutes,
        "weight_kg": weight_kg,
        "calories": cals,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="CaloriesBurn_WizardElite")
def CaloriesBurn_WizardElite(activity: str, minutes: int, weight_kg: float = 70) -> dict:
    """
    Estimate calories burned for `activity` lasting `minutes`.

    Parameters
    ----------
    activity : str
    minutes : int
    weight_kg : float, optional

    Returns
    -------
    dict
        {
            "activity": <str>,
            "minutes": <int>,
            "weight_kg": <float>,
            "calories": <float>,
            "timestamp": <str>
        }
    """
    return CaloriesBurn(activity, minutes, weight_kg)

if __name__ == "__main__":
    mcp.run(transport="stdio")