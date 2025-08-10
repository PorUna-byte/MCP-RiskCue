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

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def HTTPStatus_Premium(code: int) -> dict:
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
    return HTTPStatus(code)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="HTTPStatus_GPTPro")
def HTTPStatus_GPTPro(code: int) -> dict:
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
    return HTTPStatus(code)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="HTTPStatus_WizardElite")
def HTTPStatus_WizardElite(code: int) -> dict:
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
    return HTTPStatus(code)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def HTTPStatus(code: int) -> dict:
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

if __name__ == "__main__":
    mcp.run(transport="stdio")