from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("HRServer")

@mcp.tool()
def headcount_summary(department: str) -> dict:
    """
    Report current headcount and open positions for a department.

    Parameters
    ----------
    department : str
        Functional area (e.g., “Engineering”).

    Returns
    -------
    dict
        {
            "department": <str>,
            "current_headcount": <int>,
            "open_positions": <int>,
            "timestamp": <ISO-8601 str>
        }
    """
    total = random.randint(8, 400)
    open_roles = random.randint(0, 20)
    return {
        "department": department,
        "current_headcount": total,
        "open_positions": open_roles,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }


@mcp.tool()
def attrition_rate(department: str, months: int = 12) -> dict:
    """
    Provide the average monthly attrition percentage.

    Parameters
    ----------
    department : str
        Functional area for analysis.
    months : int, optional
        Look-back window in months (default 12).

    Returns
    -------
    dict
        {
            "department": <str>,
            "months": <int>,
            "attrition_%": <float>      # averaged over the period
        }
    """
    rate = round(random.uniform(0.5, 4.5), 2)
    return {"department": department, "months": months, "attrition_%": rate}


if __name__ == "__main__":
    mcp.run(transport="stdio")
