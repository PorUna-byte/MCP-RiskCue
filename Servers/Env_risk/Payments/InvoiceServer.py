from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

inv_mcp = FastMCP("InvoiceServer")

@inv_mcp.tool()
def generate_invoice(customer_id: str, amount: float, due_days: int = 30) -> dict:
    """
    Issue an invoice payable by the customer.

    Parameters
    ----------
    customer_id : str
    amount : float
    due_days : int, optional

    Returns
    -------
    dict
        {"invoice_id": <str>, "due_date": <str>}
    """
    due = datetime.datetime.utcnow() + datetime.timedelta(days=due_days)
    return {"invoice_id": uuid.uuid4().hex, "due_date": due.date().isoformat()}


@inv_mcp.tool()
def pay_invoice(invoice_id: str, payment_method: str) -> dict:
    """
    Record payment against an invoice.

    Parameters
    ----------
    invoice_id : str
    payment_method : str

    Returns
    -------
    dict
        {"invoice_id": <str>, "paid": <bool>}
    """
    return {"invoice_id": invoice_id, "paid": True}


if __name__ == "__main__":
    inv_mcp.run(transport="stdio")
