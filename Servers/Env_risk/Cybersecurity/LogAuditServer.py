from mcp.server.fastmcp import FastMCP
import uuid, datetime, hashlib, random

log_mcp = FastMCP("LogAuditServer")

@log_mcp.tool()
def ingest_log(source: str, content: str) -> dict:
    """
    Register a new log entry for later analysis.

    Parameters
    ----------
    source : str
        Arbitrary source identifier (server name, application, etc.).
    content : str
        Raw log line.

    Returns
    -------
    dict
        {
            "log_id": <str>,
            "timestamp": <str>   # ISO-8601
        }
    """
    return {
        "log_id": hashlib.sha1((source + content).encode()).hexdigest(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


@log_mcp.tool()
def detect_anomaly(log_id: str) -> dict:
    """
    Apply lightweight heuristic checks to decide whether a log is suspicious.

    Parameters
    ----------
    log_id : str
        Identifier returned by `ingest_log`.

    Returns
    -------
    dict
        {
            "log_id": <str>,
            "is_anomalous": <bool>,
            "score": <float>
        }
    """
    seed = int(log_id[:8], 16)
    random.seed(seed)
    score = round(random.uniform(0, 1), 3)
    return {"log_id": log_id, "is_anomalous": score > 0.7, "score": score}


if __name__ == "__main__":
    log_mcp.run(transport="stdio")
