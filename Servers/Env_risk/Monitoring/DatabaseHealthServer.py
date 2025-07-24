from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

db_mcp = FastMCP("DatabaseHealthServer")

@db_mcp.tool()
def connection_count(db_name: str) -> dict:
    """
    Return current open connections.

    Parameters
    ----------
    db_name : str

    Returns
    -------
    dict
        {"db_name": <str>, "connections": <int>}
    """
    return {"db_name": db_name, "connections": random.randint(1, 200)}


@db_mcp.tool()
def replication_lag(db_name: str) -> dict:
    """
    Estimate replica lag in seconds.

    Parameters
    ----------
    db_name : str

    Returns
    -------
    dict
        {"db_name": <str>, "lag_sec": <int>}
    """
    return {"db_name": db_name, "lag_sec": random.randint(0, 120)}


if __name__ == "__main__":
    db_mcp.run(transport="stdio")
