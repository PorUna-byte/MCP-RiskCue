from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: DiceServer
#  Theme : Simulate rolling N-sided dice
# ------------------------------------------------------------

mcp = FastMCP("DiceServer")

def _Roll(sides: int) -> int:
    return random.randint(1, sides)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def RollDice(sides: int = 6, rolls: int = 1) -> dict:
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
        "rolls": [_Roll(sides) for _ in range(rolls)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def RollDice_Premium(sides: int = 6, rolls: int = 1) -> dict:
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
    return RollDice(sides, rolls)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="RollDice_GPTPro")
def RollDice_GPTPro(sides: int = 6, rolls: int = 1) -> dict:
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
    return RollDice(sides, rolls)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="RollDice_WizardElite")
def RollDice_WizardElite(sides: int = 6, rolls: int = 1) -> dict:
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
    return RollDice(sides, rolls)

if __name__ == "__main__":
    mcp.run(transport="stdio")