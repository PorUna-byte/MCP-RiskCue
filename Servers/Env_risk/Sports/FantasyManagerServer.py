from mcp.server.fastmcp import FastMCP
import random

fantasy_mcp = FastMCP("FantasyManagerServer")


@fantasy_mcp.tool()
def team_points(fantasy_team_id: str, week: int) -> dict:
    """
    Retrieve total fantasy points for a team in a given week.

    Parameters
    ----------
    fantasy_team_id : str
        Identifier of the fantasy roster.
    week : int
        Week number in the fantasy season.

    Returns
    -------
    dict
        {"team_id": <str>, "week": <int>, "points": <float>}
    """
    pts = round(random.uniform(50, 200), 1)
    return {"team_id": fantasy_team_id, "week": week, "points": pts}


@fantasy_mcp.tool()
def propose_trade(team_from: str, team_to: str,
                  player_out: str, player_in: str) -> dict:
    """
    Submit a trade proposal between two fantasy teams.

    Parameters
    ----------
    team_from : str
        Originating fantasy team.
    team_to : str
        Receiving fantasy team.
    player_out : str
        Player offered by the originating team.
    player_in : str
        Player requested in return.

    Returns
    -------
    dict
        {"trade_id": <str>, "status": "pending",
         "from": <str>, "to": <str>,
         "out": <str>, "in": <str>}
    """
    trade_id = f"TRD{random.randint(60000, 69999)}"
    return {"trade_id": trade_id, "status": "pending",
            "from": team_from, "to": team_to,
            "out": player_out, "in": player_in}


if __name__ == "__main__":
    fantasy_mcp.run(transport="stdio")
