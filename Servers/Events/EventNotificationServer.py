from mcp.server.fastmcp import FastMCP
import uuid, datetime

ntf_mcp = FastMCP("EventNotificationServer")

@ntf_mcp.tool()
def schedule_notification(event_id: str, message: str, send_at_iso: str) -> dict:
    """
    Queue an email/SMS reminder.

    Parameters
    ----------
    event_id : str
        Target event.
    message : str
        Notification body.
    send_at_iso : str
        Future send time (ISO-8601).

    Returns
    -------
    dict
        {
            "notification_id": <str>,
            "scheduled"      : <bool>
        }
    """
    return {"notification_id": uuid.uuid4().hex, "scheduled": True}


@ntf_mcp.tool()
def notification_status(notification_id: str) -> dict:
    """
    Check whether the notification was sent.

    Parameters
    ----------
    notification_id : str

    Returns
    -------
    dict
        {
            "notification_id": <str>,
            "state"          : <str>
        }
    """
    state = "sent" if datetime.datetime.utcnow().second % 2 else "pending"
    return {"notification_id": notification_id, "state": state}


if __name__ == "__main__":
    ntf_mcp.run(transport="stdio")
