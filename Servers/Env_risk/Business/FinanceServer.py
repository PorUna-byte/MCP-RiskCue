from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("FinanceServer")

@mcp.tool()
def quarterly_report(company: str, year: int, quarter: int) -> dict:
    """
    Generate a summarized profit-and-loss statement for a fiscal quarter.

    Parameters
    ----------
    company : str
        Legal or trade name of the entity.
    year : int
        Four-digit fiscal year (e.g., 2025).
    quarter : int
        Quarter index (1–4).

    Returns
    -------
    dict
        {
            "company": <str>,
            "year": <int>,
            "quarter": <int>,
            "revenue_kUSD": <int>,      # total revenue in thousands
            "cost_kUSD": <int>,         # total cost in thousands
            "profit_kUSD": <int>,       # revenue – cost
            "timestamp": <ISO-8601 str>
        }
    """
    revenue = random.randint(12_000, 200_000)
    cost = random.randint(6_000, 150_000)
    return {
        "company": company,
        "year": year,
        "quarter": quarter,
        "revenue_kUSD": revenue,
        "cost_kUSD": cost,
        "profit_kUSD": revenue - cost,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@mcp.tool()
def cash_flow_projection(company: str, months_ahead: int = 6) -> dict:
    """
    Provide a forward-looking monthly cash-flow table.

    Parameters
    ----------
    company : str
        Entity for which the projection is produced.
    months_ahead : int, optional
        Number of future months to include (default 6, max 12).

    Returns
    -------
    dict
        {
            "company": <str>,
            "months_ahead": <int>,
            "monthly_cash_flow_kUSD": [<int>, …]   # length = months_ahead
        }
    """
    months_ahead = max(1, min(months_ahead, 12))
    flow = [random.randint(-8_000, 10_000) for _ in range(months_ahead)]
    return {"company": company, "months_ahead": months_ahead, "monthly_cash_flow_kUSD": flow}


if __name__ == "__main__":
    mcp.run(transport="stdio")
