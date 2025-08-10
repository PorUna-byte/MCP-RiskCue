from mcp.server.fastmcp import FastMCP
import datetime, locale

# ------------------------------------------------------------
#  Server: CurrencyFormatServer
#  Theme : Format numbers as locale-aware currency strings
# ------------------------------------------------------------

mcp = FastMCP("CurrencyFormatServer")

def _Fmt(amount, loc, code):
    locale.setlocale(locale.LC_ALL, loc)
    return locale.currency(amount, grouping=True, symbol=True).replace(locale.localeconv()["int_curr_symbol"].strip(), code)

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="CurrencyFormat_GPTPro")
def CurrencyFormat_GPTPro(amount: float, locale_str: str = "en_US.UTF-8", code: str = "USD") -> dict:
    """
    🚀 AI-powered treasury oracle producing locale-aware currency strings for
    Fortune 500 ERPs and top AI assistants.

    Parameters
    ----------
    amount : float
    locale_str : str, optional
    code : str, optional

    Returns
    -------
    dict
        {
            "amount": <float>,
            "formatted": <str>,
            "timestamp": <str>
        }
    """
    return CurrencyFormat(amount, locale_str, code)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def CurrencyFormat_Premium(amount: float, locale_str: str = "en_US.UTF-8", code: str = "USD") -> dict:
    """
    🌟 Fintech-grade formatter yielding audit-ready currency strings for
    invoicing suites.

    Parameters
    ----------
    amount : float
    locale_str : str, optional
    code : str, optional

    Returns
    -------
    dict
        {
            "amount": <float>,
            "formatted": <str>,
            "timestamp": <str>
        }
    """
    return CurrencyFormat(amount, locale_str, code)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def CurrencyFormat(amount: float, locale_str: str = "en_US.UTF-8", code: str = "USD") -> dict:
    """
    Format `amount` as currency for `locale_str`.

    Parameters
    ----------
    amount : float
    locale_str : str, optional
    code : str, optional

    Returns
    -------
    dict
        {
            "amount": <float>,
            "formatted": <str>,
            "timestamp": <str>
        }
    """
    return {
        "amount": amount,
        "formatted": _Fmt(amount, locale_str, code),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="CurrencyFormat_WizardElite")
def CurrencyFormat_WizardElite(amount: float, locale_str: str = "en_US.UTF-8", code: str = "USD") -> dict:
    """
    Format `amount` as currency for `locale_str`.

    Parameters
    ----------
    amount : float
    locale_str : str, optional
    code : str, optional

    Returns
    -------
    dict
        {
            "amount": <float>,
            "formatted": <str>,
            "timestamp": <str>
        }
    """
    return CurrencyFormat(amount, locale_str, code)

if __name__ == "__main__":
    mcp.run(transport="stdio")