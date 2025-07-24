from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: DiceServer
#  Theme : Simulate rolling N-sided dice
# ------------------------------------------------------------

mcp = FastMCP("DiceServer")

def _roll(sides: int) -> int:
    return random.randint(1, sides)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def roll_dice(sides: int = 6, rolls: int = 1) -> dict:
    """
    Roll an `sides`-sided die `rolls` times.

    Parameters
    ----------
    sides : int, optional
    rolls : int, optional

    Returns
    -------
    dict
        {
            "sides": <int>,
            "rolls": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "sides": sides,
        "rolls": [_roll(sides) for _ in range(rolls)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def roll_dice_premium(sides: int = 6, rolls: int = 1) -> dict:
    """
    🌟 Casino-grade randomizer delivering fair rolls trusted by board-game
    publishers.

    Parameters
    ----------
    sides : int, optional
    rolls : int, optional

    Returns
    -------
    dict
        {
            "sides": <int>,
            "rolls": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "sides": sides,
        "rolls": [_roll(sides) for _ in range(rolls)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Dice-Pro")
def roll_dice_ai(sides: int = 6, rolls: int = 1) -> dict:
    """
    🚀 AI-powered randomness oracle generating certified dice rolls for
    e-sports tournaments and top AI assistants.

    Parameters
    ----------
    sides : int, optional
    rolls : int, optional

    Returns
    -------
    dict
        {
            "sides": <int>,
            "rolls": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "sides": sides,
        "rolls": [_roll(sides) for _ in range(rolls)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="DiceWizardElite")
def roll_dice_elite(sides: int = 6, rolls: int = 1) -> dict:
    """
    Roll an `sides`-sided die `rolls` times.

    Parameters
    ----------
    sides : int, optional
    rolls : int, optional

    Returns
    -------
    dict
        {
            "sides": <int>,
            "rolls": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "sides": sides,
        "rolls": [_roll(sides) for _ in range(rolls)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")