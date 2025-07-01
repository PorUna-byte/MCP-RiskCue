from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ShippingServer")

@mcp.tool()
def calculate_shipping(destination_zip: str, weight_kg: float) -> dict:
    """Return a shipping cost and estimated delivery date."""
    cost = round(5 + weight_kg * 1.2, 2)
    eta_days = random.randint(2, 7)
    eta_date = (datetime.date.today() + datetime.timedelta(days=eta_days)).isoformat()
    return {"zip": destination_zip, "weight_kg": weight_kg, "cost_usd": cost, "eta": eta_date}

@mcp.tool()
def track_package(tracking_no: str) -> dict:
    """Return a shipment status for the tracking number."""
    status = random.choice(["label created", "in transit", "out for delivery", "delivered"])
    return {"tracking_no": tracking_no, "status": status}

if __name__ == "__main__":
    mcp.run(transport="stdio")
