from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

esp_mcp = FastMCP("EsportsScheduleServer")

@esp_mcp.tool()
def upcoming_matches(game_title: str, limit: int = 3) -> dict:
    """
    List scheduled esports matches.

    Parameters
    ----------
    game_title : str
    limit : int, optional

    Returns
    -------
    dict
        {
            "matches": [
                {"match_id": <str>, "teams": <str>, "start": <str>}, …
            ]
        }
    """
    matches = [{
        "match_id": uuid.uuid4().hex[:8],
        "teams": f"Team {i} vs Team {i+1}",
        "start": (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=i)).isoformat() + "Z",
    } for i in range(1, limit + 1)]
    return {"matches": matches}


if __name__ == "__main__":
    esp_mcp.run(transport="stdio")
