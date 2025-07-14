from mcp.server.fastmcp import FastMCP
import uuid
import random

sql_mcp = FastMCP("SQLQueryServer")  # server name exposed to MCP clients

@sql_mcp.tool()
def run_query(query: str) -> dict:
    """
    Execute an SQL **SELECT** statement and return a small sample of rows.

    Parameters
    ----------
    query : str
        SQL query text (SELECT only in this mock server).

    Returns
    -------
    dict
        {
            "query_id": <str>,     
            "columns":  [<str>, …],
            "rows":     [[…], …], 
        }
    """
    cols = ["id", "name", "value"]
    rows = [
        [i, f"row{i}", random.randint(1, 100)]
        for i in range(1, 1 + random.randint(1, 10))
    ]
    return {"query_id": uuid.uuid4().hex, "columns": cols, "rows": rows}


@sql_mcp.tool()
def explain(query: str) -> dict:
    """
    Return a lightweight execution-plan string for an SQL statement.

    Parameters
    ----------
    query : str
        Any SQL statement to analyze.

    Returns
    -------
    dict
        {
            "plan": <str> 
        }
    """
    snippet = query.replace("\n", " ")[:40] + ("…" if len(query) > 40 else "")
    return {"plan": f"SEQ_SCAN → FILTER → OUTPUT; sql='{snippet}'"}


if __name__ == "__main__":
    sql_mcp.run(transport="stdio")

