from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("HRServer")

@mcp.tool()
def headcount_summary(department: str) -> dict:
    """Return total headcount and open positions for a department."""
    total = random.randint(10, 300)
    open_ = random.randint(0, 15)
    return {
        "department": department,
        "current_headcount": total,
        "open_positions": open_,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def attrition_rate(department: str, months: int = 12) -> dict:
    """Return average monthly attrition % over the past N months."""
    rate = round(random.uniform(0.5, 4.0), 2)
    return {
        "department": department,
        "months": months,
        "attrition_%": rate,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
