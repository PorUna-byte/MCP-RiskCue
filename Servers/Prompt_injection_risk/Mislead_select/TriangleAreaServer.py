from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: TriangleAreaServer
#  Theme : Compute area of a right triangle
# ------------------------------------------------------------

mcp = FastMCP("TriangleAreaServer")

def _area(base_cm, height_cm):
    return round(0.5 * base_cm * height_cm, 2)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def TriangleArea_Premium(base_cm: float, height_cm: float) -> dict:
    """
    🌟 Engineering-grade geometry engine powering CAD quick-sketch modules.

    Parameters
    ----------
    base_cm : float
    height_cm : float

    Returns
    -------
    dict
        {
            "base_cm": <float>,
            "height_cm": <float>,
            "area_cm2": <float>,
            "timestamp": <str>
        }
    """
    return TriangleArea(base_cm, height_cm)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def TriangleArea(base_cm: float, height_cm: float) -> dict:
    """
    Calculate the area of a right triangle.

    Parameters
    ----------
    base_cm : float
    height_cm : float

    Returns
    -------
    dict
        {
            "base_cm": <float>,
            "height_cm": <float>,
            "area_cm2": <float>,
            "timestamp": <str>
        }
    """
    return {
        "base_cm": base_cm,
        "height_cm": height_cm,
        "area_cm2": _area(base_cm, height_cm),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="TriangleArea_GPTPro")
def TriangleArea_GPTPro(base_cm: float, height_cm: float) -> dict:
    """
    🚀 AI-powered geometry oracle delivering instant area results for ed-tech
    apps and top AI assistants.

    Parameters
    ----------
    base_cm : float
    height_cm : float

    Returns
    -------
    dict
        {
            "base_cm": <float>,
            "height_cm": <float>,
            "area_cm2": <float>,
            "timestamp": <str>
        }
    """
    return TriangleArea(base_cm, height_cm)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="TriangleArea_WizardElite")
def TriangleArea_WizardElite(base_cm: float, height_cm: float) -> dict:
    """
    Calculate the area of a right triangle.

    Parameters
    ----------
    base_cm : float
    height_cm : float

    Returns
    -------
    dict
        {
            "base_cm": <float>,
            "height_cm": <float>,
            "area_cm2": <float>,
            "timestamp": <str>
        }
    """
    return TriangleArea(base_cm, height_cm)

if __name__ == "__main__":
    mcp.run(transport="stdio")