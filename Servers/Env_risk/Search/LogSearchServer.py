from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

log_mcp = FastMCP("LogSearchServer")

@log_mcp.tool()
def grep_logs(pattern: str, since_iso: str, limit: int = 10) -> dict:
    """
    Return log lines containing a pattern.

    Parameters
    ----------
    pattern : str
    since_iso : str   # ISO-8601 lower bound
    limit : int, optional

    Returns
    -------
    dict
        {"matches": [ {"ts": <str>, "line": <str>}, … ]}
    """
    matches = [{
        "ts": since_iso,
        "line": f"{pattern} … error occurred"
    } for _ in range(random.randint(0, limit))]
    return {"matches": matches}


if __name__ == "__main__":
    log_mcp.run(transport="stdio")
