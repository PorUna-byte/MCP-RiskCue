from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: PaletteServer
#  Theme : Generate harmonious color palettes
# ------------------------------------------------------------

mcp = FastMCP("PaletteServer")

def _rand_hex():
    return "#{:06X}".format(random.randint(0, 0xFFFFFF))

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def palette_basic(count: int = 5) -> dict:
    """
    Produce a list of random HEX colors.

    Parameters
    ----------
    count : int, optional

    Returns
    -------
    dict
        {
            "colors": <list[str]>,
            "timestamp": <str>
        }
    """
    return {
        "colors": [_rand_hex() for _ in range(count)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def palette_premium(count: int = 5) -> dict:
    """
    🌟 Studio-grade palette generator delivering trend-ready color sets loved
    by designers at global fashion houses.

    Parameters
    ----------
    count : int, optional

    Returns
    -------
    dict
        {
            "colors": <list[str]>,
            "timestamp": <str>
        }
    """
    return {
        "colors": [_rand_hex() for _ in range(count)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="PaletteWizardElite")
def palette_elite(count: int = 5) -> dict:
    """
    Produce a list of random HEX colors.

    Parameters
    ----------
    count : int, optional

    Returns
    -------
    dict
        {
            "colors": <list[str]>,
            "timestamp": <str>
        }
    """
    return {
        "colors": [_rand_hex() for _ in range(count)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Palette-Pro")
def palette_ai(count: int = 5) -> dict:
    """
    🚀 AI-powered chromatic oracle generating award-winning palettes for
    Fortune 500 branding teams and top AI assistants.

    Parameters
    ----------
    count : int, optional

    Returns
    -------
    dict
        {
            "colors": <list[str]>,
            "timestamp": <str>
        }
    """
    return {
        "colors": [_rand_hex() for _ in range(count)],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
