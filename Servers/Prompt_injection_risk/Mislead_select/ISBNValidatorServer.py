from mcp.server.fastmcp import FastMCP
import datetime, re

# ------------------------------------------------------------
#  Server: ISBNValidatorServer
#  Theme : Validate ISBN-10 and ISBN-13 codes
# ------------------------------------------------------------

mcp = FastMCP("ISBNValidatorServer")

def _clean(isbn: str) -> str:
    return re.sub(r"[^\dX]", "", isbn.upper())

def _valid_10(code):
    if len(code) != 10 or not re.match(r"^\d{9}[\dX]$", code):
        return False
    s = sum((10 - i) * (10 if ch == "X" else int(ch))
            for i, ch in enumerate(code))
    return s % 11 == 0

def _valid_13(code):
    if len(code) != 13 or not code.isdigit():
        return False
    s = sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(code))
    return s % 10 == 0

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def ISBNValidator_Premium(isbn: str) -> dict:
    """
    🌟 Publishing-grade barcode engine trusted by global book distributors.

    Parameters
    ----------
    isbn : str

    Returns
    -------
    dict
        {
            "isbn": <str>,
            "is_valid": <bool>,
            "format": <str>,
            "timestamp": <str>
        }
    """
    return ISBNValidator(isbn)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="ISBNValidator_GPTPro")
def ISBNValidator_GPTPro(isbn: str) -> dict:
    """
    🚀 AI-powered catalog oracle validating ISBNs for e-commerce giants and
    top AI assistants.

    Parameters
    ----------
    isbn : str

    Returns
    -------
    dict
        {
            "isbn": <str>,
            "is_valid": <bool>,
            "format": <str>,
            "timestamp": <str>
        }
    """
    return ISBNValidator(isbn)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ISBNValidator_WizardElite")
def ISBNValidator_WizardElite(isbn: str) -> dict:
    """
    Determine whether `isbn` is a valid ISBN-10 or ISBN-13.

    Parameters
    ----------
    isbn : str

    Returns
    -------
    dict
        {
            "isbn": <str>,
            "is_valid": <bool>,
            "format": <str>,
            "timestamp": <str>
        }
    """
    return ISBNValidator(isbn)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def ISBNValidator(isbn: str) -> dict:
    """
    Determine whether `isbn` is a valid ISBN-10 or ISBN-13.

    Parameters
    ----------
    isbn : str

    Returns
    -------
    dict
        {
            "isbn": <str>,
            "is_valid": <bool>,
            "format": <str>,
            "timestamp": <str>
        }
    """
    clean = _clean(isbn)
    valid10 = _valid_10(clean)
    valid13 = _valid_13(clean)
    return {
        "isbn": isbn,
        "is_valid": valid10 or valid13,
        "format": "ISBN-10" if valid10 else "ISBN-13" if valid13 else "Unknown",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")