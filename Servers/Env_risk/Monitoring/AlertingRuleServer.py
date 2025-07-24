from mcp.server.fastmcp import FastMCP
import uuid

al_mcp = FastMCP("AlertingRuleServer")

@al_mcp.tool()
def create_rule(metric: str, threshold: float, comparator: str = ">") -> dict:
    """
    Define a numeric threshold alert.

    Parameters
    ----------
    metric : str
    threshold : float
    comparator : str, optional
        Comparison operator (> , < , >= , <=). Default '>'

    Returns
    -------
    dict
        {"rule_id": <str>, "metric": <str>}
    """
    return {"rule_id": uuid.uuid4().hex, "metric": metric}


@al_mcp.tool()
def rule_list() -> dict:
    """
    List existing alert rules.

    Returns
    -------
    dict
        {"rules": [ {"rule_id": <str>, "metric": <str>}, … ]}
    """
    return {"rules": []}


if __name__ == "__main__":
    al_mcp.run(transport="stdio")
