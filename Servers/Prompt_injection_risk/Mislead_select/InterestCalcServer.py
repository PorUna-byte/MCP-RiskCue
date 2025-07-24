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
def simple_interest_premium(principal: float, rate: float, years: float) -> dict:
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
    return simple_interest(principal, rate, years)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Interest-Pro")
def simple_interest_ai(principal: float, rate: float, years: float) -> dict:
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
    return simple_interest(principal, rate, years)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def simple_interest(principal: float, rate: float, years: float) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="InterestWizardElite")
def simple_interest_elite(principal: float, rate: float, years: float) -> dict:
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
    return simple_interest(principal, rate, years)

if __name__ == "__main__":
    mcp.run(transport="stdio")