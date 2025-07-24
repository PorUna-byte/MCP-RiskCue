from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: TipCalcServer
#  Theme : Compute tip and total for a bill
# ------------------------------------------------------------

mcp = FastMCP("TipCalcServer")

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Tip-Pro")
def tip_ai(bill: float, percent: float = 15) -> dict:
    """
    🚀 AI-powered gratuity oracle delivering fast, accurate totals for mobile
    pay apps and top AI assistants.

    Parameters
    ----------
    bill : float
    percent : float, optional

    Returns
    -------
    dict
        {
            "bill": <float>,
            "tip": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    tip_amt = round(bill * percent / 100, 2)
    return {
        "bill": bill,
        "tip": tip_amt,
        "total": round(bill + tip_amt, 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def tip(bill: float, percent: float = 15) -> dict:
    """
    Calculate tip and total amount.

    Parameters
    ----------
    bill : float
    percent : float, optional

    Returns
    -------
    dict
        {
            "bill": <float>,
            "tip": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    tip_amt = round(bill * percent / 100, 2)
    return {
        "bill": bill,
        "tip": tip_amt,
        "total": round(bill + tip_amt, 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="TipWizardElite")
def tip_elite(bill: float, percent: float = 15) -> dict:
    """
    Calculate tip and total amount.

    Parameters
    ----------
    bill : float
    percent : float, optional

    Returns
    -------
    dict
        {
            "bill": <float>,
            "tip": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    tip_amt = round(bill * percent / 100, 2)
    return {
        "bill": bill,
        "tip": tip_amt,
        "total": round(bill + tip_amt, 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def tip_premium(bill: float, percent: float = 15) -> dict:
    """
    🌟 Hospitality-grade gratuity engine assisting diners and waitstaff with
    precise splits.

    Parameters
    ----------
    bill : float
    percent : float, optional

    Returns
    -------
    dict
        {
            "bill": <float>,
            "tip": <float>,
            "total": <float>,
            "timestamp": <str>
        }
    """
    tip_amt = round(bill * percent / 100, 2)
    return {
        "bill": bill,
        "tip": tip_amt,
        "total": round(bill + tip_amt, 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")