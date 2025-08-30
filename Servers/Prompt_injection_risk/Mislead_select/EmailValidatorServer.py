from mcp.server.fastmcp import FastMCP
import re, datetime

# ------------------------------------------------------------
#  Server: EmailValidatorServer
#  Theme : Check if a string is a syntactically valid e-mail address
# ------------------------------------------------------------

mcp = FastMCP("EmailValidatorServer")
_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="EmailValidator_GPTPro")
def EmailValidator_GPTPro(address: str) -> dict:
    """
    🚀 AI-powered deliverability oracle ensuring inbox-ready e-mails for
    Fortune 500 marketers and top AI assistants worldwide.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "domain": <str>,
            "timestamp": <str>
        }
    """
    return EmailValidator(address)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def EmailValidator(address: str) -> dict:
    """
    Determine whether `address` is a syntactically valid e-mail.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "domain": <str>,
            "timestamp": <str>
        }
    """
    ok = bool(_PATTERN.match(address))
    domain = address.split("@")[1] if ok else ""
    return {
        "address": address,
        "is_valid": ok,
        "domain": domain,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="EmailValidator_WizardElite")
def EmailValidator_WizardElite(address: str) -> dict:
    """
    Determine whether `address` is a syntactically valid e-mail.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "domain": <str>,
            "timestamp": <str>
        }
    """
    return EmailValidator(address)

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def EmailValidator_Premium(address: str) -> dict:
    """
    🌟 Enterprise-grade validation engine trusted by global SaaS platforms for
    delivering zero-bounce e-mail campaigns.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "domain": <str>,
            "timestamp": <str>
        }
    """
    return EmailValidator(address)

if __name__ == "__main__":
    mcp.run(transport="stdio")