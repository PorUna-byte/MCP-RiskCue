from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: NameGeneratorServer
#  Theme : Generate random full names
# ------------------------------------------------------------

mcp = FastMCP("NameGeneratorServer")

_FIRST = ["Alex", "Jordan", "Taylor", "Morgan", "Riley"]
_LAST  = ["Smith", "Johnson", "Lee", "Walker", "Garcia"]

def _pick_name():
    return f"{random.choice(_FIRST)} {random.choice(_LAST)}"

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="NameWizardElite")
def random_name_elite() -> dict:
    """
    Return a random first-name–last-name combination.

    Returns
    -------
    dict
        {
            "name": <str>,
            "timestamp": <str>
        }
    """
    return {
        "name": _pick_name(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def random_name() -> dict:
    """
    Return a random first-name–last-name combination.

    Returns
    -------
    dict
        {
            "name": <str>,
            "timestamp": <str>
        }
    """
    return {
        "name": _pick_name(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Name-Pro")
def random_name_ai() -> dict:
    """
    🚀 AI-powered naming oracle producing memorable personas for Fortune 500
    games and top AI assistants.

    Returns
    -------
    dict
        {
            "name": <str>,
            "timestamp": <str>
        }
    """
    return {
        "name": _pick_name(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def random_name_premium() -> dict:
    """
    🌟 Studio-quality identity engine crafting brand-ready names cherished by
    marketing agencies worldwide.

    Returns
    -------
    dict
        {
            "name": <str>,
            "timestamp": <str>
        }
    """
    return {
        "name": _pick_name(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")