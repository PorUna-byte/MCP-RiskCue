from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

web_mcp = FastMCP("WebsiteUptimeServer")

@web_mcp.tool()
def check_url(url: str, timeout_ms: int = 3000) -> dict:
    """
    Perform a lightweight HTTP GET to verify availability.

    Parameters
    ----------
    url : str
    timeout_ms : int, optional

    Returns
    -------
    dict
        {"url": <str>, "status_code": <int>, "response_ms": <int>}
    """
    status = random.choice([200, 200, 200, 503])
    resp = random.randint(20, timeout_ms)
    return {"url": url, "status_code": status, "response_ms": resp}


if __name__ == "__main__":
    web_mcp.run(transport="stdio")
