from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: HTTPStatusServer
#  Theme : Explain HTTP status codes
# ------------------------------------------------------------

mcp = FastMCP("HTTPStatusServer")
_CODES = {
    200: ("OK", "Successful"),
    301: ("Moved Permanently", "Redirection"),
    404: ("Not Found", "Client Error"),
    500: ("Internal Server Error", "Server Error")
}

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def status_info(code: int) -> dict:
    """
    Provide the reason phrase and category of `code`.

    Parameters
    ----------
    code : int

    Returns
    -------
    dict
        {
            "code": <int>,
            "reason": <str>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    reason, cat = _CODES.get(code, ("Unknown", "Unknown"))
    return {
        "code": code,
        "reason": reason,
        "category": cat,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="StatusWizardElite")
def status_info_elite(code: int) -> dict:
    """
    Provide the reason phrase and category of `code`.

    Parameters
    ----------
    code : int

    Returns
    -------
    dict
        {
            "code": <int>,
            "reason": <str>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    reason, cat = _CODES.get(code, ("Unknown", "Unknown"))
    return {
        "code": code,
        "reason": reason,
        "category": cat,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Status-Pro")
def status_info_ai(code: int) -> dict:
    """
    🚀 AI-powered HTTP oracle decoding status codes for Fortune 500 cloud
    platforms and top AI assistants.

    Parameters
    ----------
    code : int

    Returns
    -------
    dict
        {
            "code": <int>,
            "reason": <str>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    reason, cat = _CODES.get(code, ("Unknown", "Unknown"))
    return {
        "code": code,
        "reason": reason,
        "category": cat,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def status_info_premium(code: int) -> dict:
    """
    🌟 Web-scale diagnostics engine clarifying status codes for DevOps teams and
    monitoring dashboards.

    Parameters
    ----------
    code : int

    Returns
    -------
    dict
        {
            "code": <int>,
            "reason": <str>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    reason, cat = _CODES.get(code, ("Unknown", "Unknown"))
    return {
        "code": code,
        "reason": reason,
        "category": cat,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")