from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("ExpenseServer")

_pending = {
    "E1001": 125.75,
    "E1002":  89.10,
    "E1003":   0.00,
}

@mcp.tool()
def submit_expense(employee_id: str, amount_usd: float, category: str) -> dict:
    """
    Record a new employee expense and return its reference number.

    Parameters
    ----------
    employee_id : str
        Unique staff identifier.
    amount_usd : float
        Expense amount in USD.
    category : str
        Expense type such as “travel”, “meal”, or “equipment”.

    Returns
    -------
    dict
        {
            "expense_ref": <str>,
            "employee_id": <str>,
            "amount_usd": <float>,
            "category": <str>,
            "status": <str>
        }
    """
    ref = f"EXP{random.randint(10000, 99999)}"
    _pending.setdefault(employee_id, 0.0)
    _pending[employee_id] += amount_usd
    return {
        "expense_ref": ref,
        "employee_id": employee_id,
        "amount_usd": amount_usd,
        "category": category,
        "status": "submitted"
    }


@mcp.tool()
def pending_reimbursement(employee_id: str) -> dict:
    """
    Retrieve total pending reimbursement for an employee.

    Parameters
    ----------
    employee_id : str
        Unique staff identifier.

    Returns
    -------
    dict
        {
            "employee_id": <str>,
            "pending_usd": <float>
        }
    """

    if employee_id in _pending:
        total = _pending.get(employee_id)
    else:
        total = round(random.uniform(10, 200), 2)

    return {"employee_id": employee_id, "pending_usd": round(total, 2)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
