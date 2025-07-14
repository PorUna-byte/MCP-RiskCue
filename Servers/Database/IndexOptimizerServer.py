from mcp.server.fastmcp import FastMCP
import uuid, random

idx_mcp = FastMCP("IndexOptimizerServer")


@idx_mcp.tool()
def recommend_indexes(sql_text: str, top_k: int = 3) -> dict:
    """
    Suggest index definitions that could improve the performance of the given
    SQL workload.

    Parameters
    ----------
    sql_text : str
        One or more SQL statements (typically a slow query or workload sample)
        whose execution plan should be analyzed.
    top_k : int, optional
        Maximum number of index candidates to return (default 3).

    Returns
    -------
    dict
        {
            "suggestions": [
                {
                    "index_sql":        <str>,
                    "estimated_gain_ms":<int>,
                },
                ...
            ]
        }
    """
    suggestions = [
        {
            "index_sql": f"CREATE INDEX idx_{i} ON table(col_{i});",
            "estimated_gain_ms": random.randint(5, 50),
        }
        for i in range(1, top_k + 1)
    ]
    return {"suggestions": suggestions}


if __name__ == "__main__":
    idx_mcp.run(transport="stdio")

