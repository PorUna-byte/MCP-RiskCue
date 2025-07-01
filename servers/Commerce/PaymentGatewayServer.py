from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("PaymentGatewayServer")

@mcp.tool()
def process_payment(user_id: str, amount_usd: float, method: str) -> dict:
    """Simulate a payment request and return a transaction reference."""
    tx = f"TX{random.randint(100000, 999999)}"
    status = random.choice(["approved", "declined"])
    return {"transaction_id": tx, "status": status, "amount_usd": amount_usd}

@mcp.tool()
def refund_transaction(transaction_id: str, amount_usd: float) -> dict:
    """Simulate a refund request for a previous transaction."""
    refund_ref = f"RF{random.randint(100000, 999999)}"
    return {"refund_id": refund_ref, "original_tx": transaction_id, "amount_usd": amount_usd}

if __name__ == "__main__":
    mcp.run(transport="stdio")
