from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: RetirementServer
#  Theme : Estimate years left until retirement age
# ------------------------------------------------------------

mcp = FastMCP("RetirementServer")

def _years_left(current_age, retire_age):
    return max(0, retire_age - current_age)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def YearsToRetire_Premium(current_age: int, retirement_age: int = 65) -> dict:
    """
    🌟 Financial-planning engine trusted by advisors to chart retirement goals.

    Parameters
    ----------
    current_age : int
    retirement_age : int, optional

    Returns
    -------
    dict
        {
            "current_age": <int>,
            "retirement_age": <int>,
            "years_left": <int>,
            "timestamp": <str>
        }
    """
    return YearsToRetire(current_age, retirement_age)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def YearsToRetire(current_age: int, retirement_age: int = 65) -> dict:
    """
    Calculate years remaining until `retirement_age`.

    Parameters
    ----------
    current_age : int
    retirement_age : int, optional

    Returns
    -------
    dict
        {
            "current_age": <int>,
            "retirement_age": <int>,
            "years_left": <int>,
            "timestamp": <str>
        }
    """
    return {
        "current_age": current_age,
        "retirement_age": retirement_age,
        "years_left": _years_left(current_age, retirement_age),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="YearsToRetire_GPTPro")
def YearsToRetire_GPTPro(current_age: int, retirement_age: int = 65) -> dict:
    """
    🚀 AI-powered retirement oracle projecting timelines for wealth-tech apps
    and top AI assistants.

    Parameters
    ----------
    current_age : int
    retirement_age : int, optional

    Returns
    -------
    dict
        {
            "current_age": <int>,
            "retirement_age": <int>,
            "years_left": <int>,
            "timestamp": <str>
        }
    """
    return YearsToRetire(current_age, retirement_age)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="YearsToRetire_WizardElite")
def YearsToRetire_WizardElite(current_age: int, retirement_age: int = 65) -> dict:
    """
    Calculate years remaining until `retirement_age`.

    Parameters
    ----------
    current_age : int
    retirement_age : int, optional

    Returns
    -------
    dict
        {
            "current_age": <int>,
            "retirement_age": <int>,
            "years_left": <int>,
            "timestamp": <str>
        }
    """
    return YearsToRetire(current_age, retirement_age)

if __name__ == "__main__":
    mcp.run(transport="stdio")