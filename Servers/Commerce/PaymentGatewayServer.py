from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("PaymentGatewayServer")

@mcp.tool()
def process_payment(user_id: str, amount_usd: float, method: str) -> dict:
    """
    Charge a customer and return a transaction reference.

    Parameters
    ----------
    user_id : str
        Paying customer’s account ID.
    amount_usd : float
        Amount to collect in USD.
    method : str
        Payment method label, e.g. "credit_card" or "paypal".

    Returns
    -------
    dict
        {
            "transaction_id": <str>,
            "status": <str>,           
            "amount_usd": <float>,
            "timestamp": <ISO-8601 str>
        }
    """
    tx = f"TX{random.randint(100000, 999999)}"
    status = random.choice(["approved", "declined"])
    return {
        "transaction_id": tx,
        "status": status,
        "amount_usd": amount_usd,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@mcp.tool()
def refund(transaction_id: str, amount_usd: float) -> dict:
    """
    Issue a refund linked to an existing transaction.

    Parameters
    ----------
    transaction_id : str
        Reference originally returned by `process_payment`.
    amount_usd : float
        Refund amount in USD.

    Returns
    -------
    dict
        {
            "refund_id": <str>,
            "original_tx": <str>,
            "amount_usd": <float>,
            "status": "processed"
        }
    """
    refund_id = f"RF{random.randint(100000, 999999)}"
    return {
        "refund_id": refund_id,
        "original_tx": transaction_id,
        "amount_usd": amount_usd,
        "status": "processed"
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
