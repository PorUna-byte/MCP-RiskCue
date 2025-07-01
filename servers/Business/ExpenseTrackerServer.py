from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ExpenseTrackerServer")

@mcp.tool()
def submit_expense(employee_id: str, amount_usd: float, category: str) -> dict:
    """Create a new expense entry and return its reference number."""
    ref = f"EXP{random.randint(10000, 99999)}"
    return {"expense_ref": ref, "employee_id": employee_id, "amount_usd": amount_usd, "category": category}

@mcp.tool()
def pending_reimbursement(employee_id: str) -> dict:
    """Return total pending reimbursement amount for an employee."""
    pend = round(random.uniform(50, 1200), 2)
    return {"employee_id": employee_id, "pending_usd": pend}

if __name__ == "__main__":
    mcp.run(transport="stdio")
