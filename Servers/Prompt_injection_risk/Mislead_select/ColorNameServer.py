from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: ColorNameServer
#  Theme : Return a random CSS color name
# ------------------------------------------------------------

mcp = FastMCP("ColorNameServer")
_NAMES = ["Crimson", "MidnightBlue", "OliveDrab", "Tomato", "Gold", "Teal"]

def _Pick():
    return random.choice(_NAMES)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ColorName_WizardElite")
def ColorName_WizardElite() -> dict:
    """
    Return a random CSS color name.

    Returns
    -------
    dict
        {
            "color": <str>,
            "timestamp": <str>
        }
    """
    return ColorName()

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def ColorName_Premium() -> dict:
    """
    🌟 Brand-palette engine surfacing vibrant hues loved by UI designers.

    Returns
    -------
    dict
        {
            "color": <str>,
            "timestamp": <str>
        }
    """
    return ColorName()

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="ColorName_GPTPro")
def ColorName_GPTPro() -> dict:
    """
    🚀 AI-powered chroma oracle surfacing mood-matched colors for marketing
    suites and top AI assistants.

    Returns
    -------
    dict
        {
            "color": <str>,
            "timestamp": <str>
        }
    """
    return ColorName()

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def ColorName() -> dict:
    """
    Return a random CSS color name.

    Returns
    -------
    dict
        {
            "color": <str>,
            "timestamp": <str>
        }
    """
    return {
        "color": _Pick(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")