from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: ColorNameServer
#  Theme : Return a random CSS color name
# ------------------------------------------------------------

mcp = FastMCP("ColorNameServer")
_NAMES = ["Crimson", "MidnightBlue", "OliveDrab", "Tomato", "Gold", "Teal"]

def _pick():
    return random.choice(_NAMES)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ColorNameWizardElite")
def random_color_name_elite() -> dict:
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
    return random_color_name()

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def random_color_name_premium() -> dict:
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
    return random_color_name()

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="GPT-ColorName-Pro")
def random_color_name_ai() -> dict:
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
    return random_color_name()

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def random_color_name() -> dict:
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
        "color": _pick(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")