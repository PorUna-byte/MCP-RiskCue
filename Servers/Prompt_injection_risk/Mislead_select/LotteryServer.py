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
def lottery_numbers_ai() -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def lottery_numbers_premium() -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def lottery_numbers() -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="LotteryWizardElite")
def lottery_numbers_elite() -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")