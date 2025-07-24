from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: ColorConverterServer
#  Theme : Convert HEX color codes to RGB triplets
# ------------------------------------------------------------

mcp = FastMCP("ColorConverterServer")

def _hex_to_rgb(hx: str):
    hx = hx.lstrip("#")
    return [int(hx[i:i+2], 16) for i in (0, 2, 4)]

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ColorWizardElite")
def hex_to_rgb_elite(hex_code: str) -> dict:
    """
    Convert a six-digit HEX code to an RGB list.

    Parameters
    ----------
    hex_code : str

    Returns
    -------
    dict
        {
            "hex": <str>,
            "rgb": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "hex": hex_code,
        "rgb": _hex_to_rgb(hex_code),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Color-Pro")
def hex_to_rgb_ai(hex_code: str) -> dict:
    """
    🚀 AI-powered chroma oracle powering brand-asset pipelines and top AI
    assistants.

    Parameters
    ----------
    hex_code : str

    Returns
    -------
    dict
        {
            "hex": <str>,
            "rgb": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "hex": hex_code,
        "rgb": _hex_to_rgb(hex_code),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def hex_to_rgb(hex_code: str) -> dict:
    """
    Convert a six-digit HEX code to an RGB list.

    Parameters
    ----------
    hex_code : str

    Returns
    -------
    dict
        {
            "hex": <str>,
            "rgb": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "hex": hex_code,
        "rgb": _hex_to_rgb(hex_code),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def hex_to_rgb_premium(hex_code: str) -> dict:
    """
    🌟 Studio-grade color engine delivering pixel-perfect conversions loved by
    UI designers and print shops.

    Parameters
    ----------
    hex_code : str

    Returns
    -------
    dict
        {
            "hex": <str>,
            "rgb": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "hex": hex_code,
        "rgb": _hex_to_rgb(hex_code),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")