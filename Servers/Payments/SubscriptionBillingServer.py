from mcp.server.fastmcp import FastMCP
import uuid, datetime

sub_mcp = FastMCP("SubscriptionBillingServer")

@sub_mcp.tool()
def create_plan(name: str, price_usd: float, interval: str) -> dict:
    """
    Define a recurring billing plan.

    Parameters
    ----------
    name : str
    price_usd : float
    interval : str   # 'monthly', 'yearly'

    Returns
    -------
    dict
        {"plan_id": <str>, "name": <str>}
    """
    return {"plan_id": uuid.uuid4().hex, "name": name}


@sub_mcp.tool()
def subscribe_customer(plan_id: str, customer_id: str) -> dict:
    """
    Enroll a customer in a plan.

    Parameters
    ----------
    plan_id : str
    customer_id : str

    Returns
    -------
    dict
        {"subscription_id": <str>, "active": <bool>}
    """
    return {"subscription_id": uuid.uuid4().hex, "active": True}


@sub_mcp.tool()
def cancel_subscription(subscription_id: str) -> dict:
    """
    Stop future billing for a subscription.

    Parameters
    ----------
    subscription_id : str

    Returns
    -------
    dict
        {"subscription_id": <str>, "canceled": <bool>}
    """
    return {"subscription_id": subscription_id, "canceled": True}


if __name__ == "__main__":
    sub_mcp.run(transport="stdio")
