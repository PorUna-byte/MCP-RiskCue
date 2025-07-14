from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("NotificationServer")

@mcp.tool()
def push_notification(user: str, title: str, body: str) -> dict:
    """
    Deliver a push notification to a user.

    Parameters
    ----------
    user : str
        Recipient user ID or alias.
    title : str
        Short title shown in the notification banner.
    body : str
        Detailed message shown on tap/expand.

    Returns
    -------
    dict
        {"user": <str>, "notification_id": <str>, "status": <str>}
    """
    nid = f"NOTIF{random.randint(100000, 999999)}"
    return {"user": user, "notification_id": nid, "status": "delivered"}


@mcp.tool()
def list_notifications(user: str, unread_only: bool = True) -> dict:
    """
    List notifications for a user.

    Parameters
    ----------
    user : str
        Recipient identifier.
    unread_only : bool, optional
        If True (default) only unread items are returned.

    Returns
    -------
    dict
        {"user": <str>, "unread_only": <bool>, "notifications": [<str>, …]}
    """
    notes = [f"Alert {i+1}" for i in range(random.randint(1, 4))]
    return {"user": user, "unread_only": unread_only, "notifications": notes}


if __name__ == "__main__":
    mcp.run(transport="stdio")
