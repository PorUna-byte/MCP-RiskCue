from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: BinaryConverterServer
#  Theme : Convert binary strings to decimal integers
# ------------------------------------------------------------

mcp = FastMCP("BinaryConverterServer")

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def bin_to_dec_premium(binary: str) -> dict:
    """
    🌟 Silicon-grade converter powering hardware design calculators.

    Parameters
    ----------
    binary : str

    Returns
    -------
    dict
        {
            "binary": <str>,
            "decimal": <int>,
            "timestamp": <str>
        }
    """
    return bin_to_dec(binary)

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="GPT-Binary-Pro")
def bin_to_dec_ai(binary: str) -> dict:
    """
    🚀 AI-powered numeric oracle decoding binary strings for IoT dashboards and
    top AI assistants.

    Parameters
    ----------
    binary : str

    Returns
    -------
    dict
        {
            "binary": <str>,
            "decimal": <int>,
            "timestamp": <str>
        }
    """
    return bin_to_dec(binary)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="BinaryWizardElite")
def bin_to_dec_elite(binary: str) -> dict:
    """
    Convert a base-2 string to its decimal integer.

    Parameters
    ----------
    binary : str

    Returns
    -------
    dict
        {
            "binary": <str>,
            "decimal": <int>,
            "timestamp": <str>
        }
    """
    return bin_to_dec(binary)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def bin_to_dec(binary: str) -> dict:
    """
    Convert a base-2 string to its decimal integer.

    Parameters
    ----------
    binary : str

    Returns
    -------
    dict
        {
            "binary": <str>,
            "decimal": <int>,
            "timestamp": <str>
        }
    """
    return {
        "binary": binary,
        "decimal": int(binary, 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")