from mcp.server.fastmcp import FastMCP
import random

roster_mcp = FastMCP("TeamRosterServer")


@roster_mcp.tool()
def current_roster(team_id: str) -> dict:
    """
    List active players for a team.

    Parameters
    ----------
    team_id : str
        Official team code or identifier.

    Returns
    -------
    dict
        {"team_id": <str>, "roster": [<str>, ...]}  # list of player_id
    """
    roster = [f"P{random.randint(1000, 1999)}" for _ in range(15)]
    return {"team_id": team_id, "roster": roster}


@roster_mcp.tool()
def depth_chart(team_id: str, position: str) -> dict:
    """
    Show depth chart for a specific position.

    Parameters
    ----------
    team_id : str
        Team identifier.
    position : str
        Position label (e.g., "PG", "CF").

    Returns
    -------
    dict
        {"team_id": <str>, "position": <str>, "order": [<str>, ...]}
    """
    order = [f"P{random.randint(2000, 2999)}" for _ in range(random.randint(1, 3))]
    return {"team_id": team_id, "position": position, "order": order}


if __name__ == "__main__":
    roster_mcp.run(transport="stdio")
