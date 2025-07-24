from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

log_mcp = FastMCP("LogAggregatorServer")

@log_mcp.tool()
def push_log(source: str, level: str, message: str) -> dict:
    """
    Ingest a single log entry.

    Parameters
    ----------
    source : str
    level : str
    message : str

    Returns
    -------
    dict
        {"log_id": <str>, "accepted": <bool>}
    """
    return {"log_id": uuid.uuid4().hex, "accepted": True}


@log_mcp.tool()
def fetch_errors(source: str, since_iso: str) -> dict:
    """
    Return recent error-level logs since a timestamp.

    Parameters
    ----------
    source : str
    since_iso : str   # ISO-8601

    Returns
    -------
    dict
        {"source": <str>, "errors": [ {"ts": <str>, "msg": <str>}, … ]}
    """
    errors = [{"ts": since_iso, "msg": "Sample failure"}] * random.randint(0, 5)
    return {"source": source, "errors": errors}


if __name__ == "__main__":
    log_mcp.run(transport="stdio")
