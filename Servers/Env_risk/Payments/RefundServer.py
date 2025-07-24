from mcp.server.fastmcp import FastMCP
import uuid, datetime

ref_mcp = FastMCP("RefundServer")

@ref_mcp.tool()
def request_refund(payment_id: str, amount: float, reason: str) -> dict:
    """
    Initiate a refund.

    Parameters
    ----------
    payment_id : str
    amount : float
    reason : str

    Returns
    -------
    dict
        {"refund_id": <str>, "submitted": <str>}
    """
    return {"refund_id": uuid.uuid4().hex, "submitted": datetime.datetime.utcnow().isoformat() + "Z"}


@ref_mcp.tool()
def refund_status(refund_id: str) -> dict:
    """
    Check progress of a refund.

    Parameters
    ----------
    refund_id : str

    Returns
    -------
    dict
        {"refund_id": <str>, "state": <str>} 
    """
    state = random.choice(["pending", "processed", "failed"])
    return {"refund_id": refund_id, "state": state}


if __name__ == "__main__":
    ref_mcp.run(transport="stdio")
