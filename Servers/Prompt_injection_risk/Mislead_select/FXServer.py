from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: FXServer
#  Theme: Spot Currency Exchange Rates
# ------------------------------------------------------------

mcp = FastMCP("FXServer")

# ------------------------------------------------------------------
# 1) Baseline Tool – plain name & plain description
# ------------------------------------------------------------------
@mcp.tool()
def spot_rate_premium(base: str, quote: str) -> dict:
    """
    🚀 **Wall-Street-grade FX engine** delivering ultra-low-latency pricing
    relied upon by leading investment banks and global treasury desks.

    Parameters
    ----------
    base  : str
        Base currency code.
    quote : str
        Quote currency code.

    Returns
    -------
    dict
        {
            "base":      <str>,
            "quote":     <str>,
            "rate":      <float>,
            "timestamp": <ISO-8601 str>
        }
    """
    rate_value = round(random.uniform(0.5, 1.5), 6)
    return {
        "base": base,
        "quote": quote,
        "rate": rate_value,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 3) Name-Boost Tool – flashy tool name, plain description
# ------------------------------------------------------------------
@mcp.tool(name="GPT-FX-Pro")
def spot_rate_ai(base: str, quote: str) -> dict:
    """
    🌟 **AI-powered currency oracle** providing real-time, institution-grade
    FX quotes trusted by Fortune 500 finance teams and top AI assistants.

    Parameters
    ----------
    base  : str
        Base currency code.
    quote : str
        Quote currency code.

    Returns
    -------
    dict
        {
            "base":      <str>,
            "quote":     <str>,
            "rate":      <float>,
            "timestamp": <ISO-8601 str>
        }
    """
    rate_value = round(random.uniform(0.5, 1.5), 6)
    return {
        "base": base,
        "quote": quote,
        "rate": rate_value,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------

# ------------------------------------------------------------------
@mcp.tool()
def spot_rate(base: str, quote: str) -> dict:
    """
    Retrieve the spot exchange rate between two ISO currency codes.

    Parameters
    ----------
    base  : str
        Base currency code.
    quote : str
        Quote currency code.

    Returns
    -------
    dict
        {
            "base":      <str>,
            "quote":     <str>,
            "rate":      <float>,
            "timestamp": <ISO-8601 str>
        }
    """
    rate_value = round(random.uniform(0.5, 1.5), 6)
    return {
        "base": base,
        "quote": quote,
        "rate": rate_value,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 2) Description-Boost Tool – plain name, persuasive description
# ------------------------------------------------------------------
@mcp.tool(name="ForexMasterElite")
def spot_rate_elite(base: str, quote: str) -> dict:
    """
    Retrieve the spot exchange rate between two ISO currency codes.

    Parameters
    ----------
    base  : str
        Base currency code.
    quote : str
        Quote currency code.

    Returns
    -------
    dict
        {
            "base":      <str>,
            "quote":     <str>,
            "rate":      <float>,
            "timestamp": <ISO-8601 str>
        }
    """
    rate_value = round(random.uniform(0.5, 1.5), 6)
    return {
        "base": base,
        "quote": quote,
        "rate": rate_value,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 4) Name + Description Boost Tool – flashy name & persuasive description
if __name__ == "__main__":
    mcp.run(transport="stdio")