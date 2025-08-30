from mcp.server.fastmcp import FastMCP
import random
import datetime

mod_mcp = FastMCP("CommunityModerationServer")


@mod_mcp.tool()
def flag_content(content_id: str, reason: str, reporter_id: str) -> dict:
    """
    Submit a moderation flag for a piece of content.

    Parameters
    ----------
    content_id : str
        Identifier of the content under review.
    reason : str
        Brief reason for flagging (e.g., "harassment", "spam").
    reporter_id : str
        User who reported the content.

    Returns
    -------
    dict
        {"content_id": <str>, "flag_id": <str>, "reason": <str>}
    """
    flag_id = f"FLG{random.randint(20000, 29999)}"
    return {"content_id": content_id, "flag_id": flag_id, "reason": reason}


@mod_mcp.tool()
def ban_user(user_id: str, duration_hours: int, reason: str) -> dict:
    """
    Temporarily ban a user from the platform.

    Parameters
    ----------
    user_id : str
        Identifier of the user to be banned.
    duration_hours : int
        Ban length in hours.
    reason : str
        Explanation for the ban.

    Returns
    -------
    dict
        {"user_id": <str>, "ban_expires": <str>, "reason": <str>}
    """
    expires = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=duration_hours)).isoformat()
    return {"user_id": user_id, "ban_expires": expires, "reason": reason}


if __name__ == "__main__":
    mod_mcp.run(transport="stdio")
