from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: LotteryServer
#  Theme : Generate random lottery numbers
# ------------------------------------------------------------

mcp = FastMCP("LotteryServer")

def _pick():
    return sorted(random.sample(range(1, 50), 6))

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Lottery-Pro")
def LotteryNumbers_AI() -> dict:
    """
    🚀 AI-powered luck oracle producing jackpot-ready combinations for global
    gaming apps and top AI assistants.

    Returns
    -------
    dict
        {
            "numbers": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "numbers": _pick(),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def LotteryNumbers_Premium() -> dict:
    """
    🌟 Casino-grade RNG engine delivering fair picks adored by sweepstakes
    platforms.

    Returns
    -------
    dict
        {
            "numbers": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "numbers": _pick(),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def LotteryNumbers() -> dict:
    """
    Generate six unique numbers between 1 and 49.

    Returns
    -------
    dict
        {
            "numbers": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "numbers": _pick(),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="LotteryWizardElite")
def LotteryNumbers_WizardElite() -> dict:
    """
    Generate six unique numbers between 1 and 49.

    Returns
    -------
    dict
        {
            "numbers": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "numbers": _pick(),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")