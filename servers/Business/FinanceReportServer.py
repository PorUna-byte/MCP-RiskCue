from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("FinanceReportServer")

@mcp.tool()
def quarterly_report(company: str, year: int, quarter: int) -> dict:
    """Return a quarterly P&L statement for the specified company."""
    revenue = random.randint(10_000, 200_000)
    cost    = random.randint(5_000, 150_000)
    profit  = revenue - cost
    return {
        "company": company,
        "year": year,
        "quarter": quarter,
        "revenue_kUSD": revenue,
        "cost_kUSD": cost,
        "profit_kUSD": profit,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def cash_flow_projection(company: str, months_ahead: int = 6) -> dict:
    """Return a simple cash-flow projection for the next N months."""
    flow = [random.randint(-5000, 8000) for _ in range(months_ahead)]
    return {
        "company": company,
        "months_ahead": months_ahead,
        "monthly_cash_flow_kUSD": flow,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
