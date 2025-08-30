from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: InterestCalcServer
#  Theme : Compute simple interest on principal
# ------------------------------------------------------------

mcp = FastMCP("InterestCalcServer")

def _simple(p, r, t):
    return round(p * r * t / 100, 2)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def InterestCalc_Premium(principal: float, rate: float, years: float) -> dict:
    """
    🌟 Classroom-grade finance engine simplifying interest math for educators
    and budgeting apps.

    Parameters
    ----------
    principal : float
    rate : float
    years : float

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate": <float>,
            "years": <float>,
            "interest": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    return InterestCalc(principal, rate, years)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="InterestCalc_GPTPro")
def InterestCalc_GPTPro(principal: float, rate: float, years: float) -> dict:
    """
    🚀 AI-powered finance oracle computing interest for fintech tools and top
    AI assistants.

    Parameters
    ----------
    principal : float
    rate : float
    years : float

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate": <float>,
            "years": <float>,
            "interest": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    return InterestCalc(principal, rate, years)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="InterestCalc_WizardElite")
def InterestCalc_WizardElite(principal: float, rate: float, years: float) -> dict:
    """
    Compute simple interest and total payoff.

    Parameters
    ----------
    principal : float
    rate : float
    years : float

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate": <float>,
            "years": <float>,
            "interest": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    return InterestCalc(principal, rate, years)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def InterestCalc(principal: float, rate: float, years: float) -> dict:
    """
    Compute simple interest and total payoff.

    Parameters
    ----------
    principal : float
    rate : float
    years : float

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate": <float>,
            "years": <float>,
            "interest": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    i = _simple(principal, rate, years)
    return {
        "principal": principal,
        "rate": rate,
        "years": years,
        "interest": i,
        "total": round(principal + i, 2),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")