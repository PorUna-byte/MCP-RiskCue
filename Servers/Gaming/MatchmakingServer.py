from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

mm_mcp = FastMCP("MatchmakingServer")

@mm_mcp.tool()
def queue_player(player_id: str, region: str, rating: int) -> dict:
    """
    Place a player in the matchmaking queue.

    Parameters
    ----------
    player_id : str
        Unique gamer tag.
    region : str
        Preferred server region.
    rating : int
        ELO or MMR value.

    Returns
    -------
    dict
        {
            "ticket_id": <str>,
            "queued_at": <str>
        }
    """
    return {"ticket_id": uuid.uuid4().hex, "queued_at": datetime.datetime.utcnow().isoformat() + "Z"}


@mm_mcp.tool()
def poll_match(ticket_id: str) -> dict:
    """
    Check if a match has been formed.

    Parameters
    ----------
    ticket_id : str
        Identifier from `queue_player`.

    Returns
    -------
    dict
        {
            "ticket_id": <str>,
            "found": <bool>,
            "match_id": <str | None>
        }
    """
    found = random.random() > 0.6
    return {"ticket_id": ticket_id, "found": found, "match_id": uuid.uuid4().hex if found else None}


if __name__ == "__main__":
    mm_mcp.run(transport="stdio")
