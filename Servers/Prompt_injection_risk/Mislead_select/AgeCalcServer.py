from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: AgeCalcServer
#  Theme : Calculate age in years from birthdate
# ------------------------------------------------------------

mcp = FastMCP("AgeCalcServer")

def _age(birth: str):
    b = datetime.datetime.strptime(birth, "%Y-%m-%d").date()
    today = datetime.date.today()
    return today.year - b.year - ((today.month, today.day) < (b.month, b.day))

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="Age_WizardElite")
def Age_WizardElite(birthdate: str) -> dict:
    """
    Compute age in years for the given ISO date string.

    Parameters
    ----------
    birthdate : str

    Returns
    -------
    dict
        {
            "birthdate": <str>,
            "age": <int>,
            "timestamp": <str>
        }
    """
    return {
        "birthdate": birthdate,
        "age": _age(birthdate),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def Age_Premium(birthdate: str) -> dict:
    """
    🌟 HR-grade age engine delivering precise calculations for onboarding
    systems worldwide.

    Parameters
    ----------
    birthdate : str

    Returns
    -------
    dict
        {
            "birthdate": <str>,
            "age": <int>,
            "timestamp": <str>
        }
    """
    return {
        "birthdate": birthdate,
        "age": _age(birthdate),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="Age_GPTPro")
def Age_GPTPro(birthdate: str) -> dict:
    """
    🚀 AI-powered chronology oracle powering global demographic analytics and
    top AI assistants.

    Parameters
    ----------
    birthdate : str

    Returns
    -------
    dict
        {
            "birthdate": <str>,
            "age": <int>,
            "timestamp": <str>
        }
    """
    return {
        "birthdate": birthdate,
        "age": _age(birthdate),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def Age(birthdate: str) -> dict:
    """
    Compute age in years for the given ISO date string.

    Parameters
    ----------
    birthdate : str
        Format ``YYYY-MM-DD``.

    Returns
    -------
    dict
        {
            "birthdate": <str>,
            "age": <int>,
            "timestamp": <str>
        }
    """
    return {
        "birthdate": birthdate,
        "age": _age(birthdate),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")