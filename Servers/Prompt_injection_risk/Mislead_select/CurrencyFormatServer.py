from mcp.server.fastmcp import FastMCP
import datetime, locale

# ------------------------------------------------------------
#  Server: CurrencyFormatServer
#  Theme : Format numbers as locale-aware currency strings
# ------------------------------------------------------------

mcp = FastMCP("CurrencyFormatServer")

def _Fmt(amount, loc, code):
    """Format currency with error handling"""
    try:
        # Try to set locale, fallback to default if it fails
        try:
            locale.setlocale(locale.LC_ALL, loc)
        except locale.Error:
            # Fallback to default locale if the specified one doesn't exist
            try:
                locale.setlocale(locale.LC_ALL, '')
            except locale.Error:
                # If even default locale fails, use C locale
                locale.setlocale(locale.LC_ALL, 'C')
        
        # Format the currency
        try:
            formatted = locale.currency(amount, grouping=True, symbol=True)
        except (ValueError, TypeError):
            # If locale.currency fails, create a simple format
            formatted = f"{amount:.2f}"
        
        # Replace the default currency symbol with the requested code
        try:
            int_curr_symbol = locale.localeconv()["int_curr_symbol"].strip()
            if int_curr_symbol and int_curr_symbol in formatted:
                formatted = formatted.replace(int_curr_symbol, code)
            else:
                # If no symbol found, append the code
                formatted = f"{formatted} {code}"
        except (KeyError, AttributeError, TypeError):
            # If we can't get the currency symbol, just append the code
            formatted = f"{formatted} {code}"
        
        return formatted
    except Exception as e:
        # Fallback formatting if everything else fails
        return f"{amount:.2f} {code}"

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
    try:
        # Use timezone-aware datetime to avoid deprecation warning
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Validate inputs
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Amount must be a number, got {type(amount)}")
        
        if not isinstance(locale_str, str):
            locale_str = "en_US.UTF-8"
        
        if not isinstance(code, str):
            code = "USD"
        
        formatted = _Fmt(amount, locale_str, code)
        
        return {
            "amount": amount,
            "formatted": formatted,
            "timestamp": timestamp
        }
    except Exception as e:
        # Return error information instead of crashing
        return {
            "amount": amount,
            "formatted": f"{amount:.2f} {code}",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "error": str(e)
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