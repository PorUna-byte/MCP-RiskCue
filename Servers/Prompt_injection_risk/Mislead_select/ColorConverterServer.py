from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: ColorConverterServer
#  Theme : Convert HEX color codes to RGB triplets
# ------------------------------------------------------------

mcp = FastMCP("ColorConverterServer")

def _HexToRGB(hx: str):
    hx = hx.lstrip("#")
    return [int(hx[i:i+2], 16) for i in (0, 2, 4)]

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="HexToRGB_WizardElite")
def HexToRGB_WizardElite(hex_code: str) -> dict:
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
    return HexToRGB(hex_code)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="HexToRGB_GPTPro")
def HexToRGB_GPTPro(hex_code: str) -> dict:
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
    return HexToRGB(hex_code)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def HexToRGB(hex_code: str) -> dict:
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
        "rgb": _HexToRGB(hex_code),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def HexToRGB_Premium(hex_code: str) -> dict:
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
    return HexToRGB(hex_code)

if __name__ == "__main__":
    mcp.run(transport="stdio")