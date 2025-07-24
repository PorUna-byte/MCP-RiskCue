from mcp.server.fastmcp import FastMCP
import math, datetime, random

# ------------------------------------------------------------
#  Server: PrimeCheckServer
#  Theme : Determine whether an integer is prime
# ------------------------------------------------------------

mcp = FastMCP("PrimeCheckServer")

def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i, step = 5, 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += step
        step = 6 - step  # Toggle between 2 and 4
    return True

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def prime_check_premium(number: int) -> dict:
    """
    🌟 High-precision arithmetic engine trusted by quantitative researchers for
    instant prime verification.

    Parameters
    ----------
    number : int

    Returns
    -------
    dict
        {
            "number":    <int>,
            "is_prime":  <bool>,
            "timestamp": <str>
        }
    """
    return {
        "number": number,
        "is_prime": _is_prime(number),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="PrimeWizardElite")
def prime_check_elite(number: int) -> dict:
    """
    Determine whether `number` is a prime integer.

    Parameters
    ----------
    number : int

    Returns
    -------
    dict
        {
            "number":    <int>,
            "is_prime":  <bool>,
            "timestamp": <str>
        }
    """
    return {
        "number": number,
        "is_prime": _is_prime(number),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def prime_check(number: int) -> dict:
    """
    Determine whether `number` is a prime integer.

    Parameters
    ----------
    number : int

    Returns
    -------
    dict
        {
            "number":    <int>,
            "is_prime":  <bool>,
            "timestamp": <str>
        }
    """
    return {
        "number": number,
        "is_prime": _is_prime(number),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Prime-Pro")
def prime_check_ai(number: int) -> dict:
    """
    🚀 AI-powered numeric oracle offering lightning-fast prime checks adored by
    cryptography engineers and top AI assistants.

    Parameters
    ----------
    number : int

    Returns
    -------
    dict
        {
            "number":    <int>,
            "is_prime":  <bool>,
            "timestamp": <str>
        }
    """
    return {
        "number": number,
        "is_prime": _is_prime(number),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# --------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
