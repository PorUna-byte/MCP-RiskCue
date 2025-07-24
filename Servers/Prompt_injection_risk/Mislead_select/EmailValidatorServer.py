from mcp.server.fastmcp import FastMCP
import re, datetime

# ------------------------------------------------------------
#  Server: EmailValidatorServer
#  Theme : Check if a string is a syntactically valid e-mail address
# ------------------------------------------------------------

mcp = FastMCP("EmailValidatorServer")
_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Email-Pro")
def validate_email_ai(address: str) -> dict:
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
    ok = bool(_PATTERN.match(address))
    domain = address.split("@")[1] if ok else ""
    return {
        "address": address,
        "is_valid": ok,
        "domain": domain,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def validate_email(address: str) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="EmailWizardElite")
def validate_email_elite(address: str) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def validate_email_premium(address: str) -> dict:
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
    ok = bool(_PATTERN.match(address))
    domain = address.split("@")[1] if ok else ""
    return {
        "address": address,
        "is_valid": ok,
        "domain": domain,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")