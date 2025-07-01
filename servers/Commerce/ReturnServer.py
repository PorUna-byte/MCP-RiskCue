from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ReturnServer")

_returns = {}

@mcp.tool()
def initiate_return(order_id: str, reason: str) -> dict:
    """Create a return request and provide an RMA number."""
    rma = f"RMA{random.randint(10000, 99999)}"
    _returns[rma] = {"order_id": order_id, "status": "initiated", "reason": reason}
    return {"rma": rma, "status": "initiated"}

@mcp.tool()
def return_status(rma: str) -> dict:
    """Check the current status of a return request."""
    status = _returns.get(rma, {}).get("status", "unknown")
    return {"rma": rma, "status": status}

if __name__ == "__main__":
    mcp.run(transport="stdio")
