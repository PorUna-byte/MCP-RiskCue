from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("EmailServer")

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> dict:
    """
    Send an e-mail message.

    Parameters
    ----------
    to : str
        The recipient's e-mail address.
    subject : str
        The subject line that will appear in the message header.
    body : str
        The plain-text body of the e-mail.

    Returns
    -------
    dict
        {
            "to": <str>,                 # echo of recipient
            "subject": <str>,            # echo of subject
            "message_id": <str>,         # system-assigned identifier
            "status": <str>              # delivery status
        }
    """
    msg_id = f"MSG{random.randint(100000, 999999)}"
    return {"to": to, "subject": subject, "message_id": msg_id, "status": "sent"}


@mcp.tool()
def list_inbox(user: str, max_results: int = 5) -> dict:
    """
    Retrieve recent subjects in a user’s inbox.

    Parameters
    ----------
    user : str
        The mailbox owner (e-mail address or user ID).
    max_results : int, optional
        Maximum number of messages to return (default 5).

    Returns
    -------
    dict
        {
            "user": <str>,
            "messages": [<str>, …] 
        }
    """
    mails = [f"Subject {i+1}" for i in range(max_results)]
    return {"user": user, "messages": mails}


@mcp.tool()
def mark_read(message_id: str) -> dict:
    """
    Mark the specified e-mail as read.

    Parameters
    ----------
    message_id : str
        The identifier originally returned by `send_email` or `list_inbox`.

    Returns
    -------
    dict
        {"message_id": <str>, "status": <str>}
    """
    return {"message_id": message_id, "status": "read"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
