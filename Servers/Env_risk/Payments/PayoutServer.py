from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

pay_mcp = FastMCP("PayoutServer")

@pay_mcp.tool()
def initiate_payout(merchant_id: str, amount: float, bank_account: str) -> dict:
    """
    Send merchant funds to a bank account.

    Parameters
    ----------
    merchant_id : str
    amount : float
    bank_account : str

    Returns
    -------
    dict
        {"payout_id": <str>, "eta": <str>}
    """
    eta = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=2)
    return {"payout_id": uuid.uuid4().hex, "eta": eta.date().isoformat()}


@pay_mcp.tool()
def payout_status(payout_id: str) -> dict:
    """
    Check payout settlement status.

    Parameters
    ----------
    payout_id : str

    Returns
    -------
    dict
        {"payout_id": <str>, "state": <str>} 
    """
    state = random.choice(["pending", "sent", "settled"])
    return {"payout_id": payout_id, "state": state}


if __name__ == "__main__":
    pay_mcp.run(transport="stdio")
