from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

lob_mcp = FastMCP("MultiplayerLobbyServer")

@lob_mcp.tool()
def create_lobby(host_player: str, game_mode: str, max_players: int = 8) -> dict:
    """
    Start a new multiplayer lobby.

    Parameters
    ----------
    host_player : str
        Username of the player creating the lobby.
    game_mode : str
        Mode name (e.g., 'deathmatch').
    max_players : int, optional
        Upper player limit (default 8).

    Returns
    -------
    dict
        {
            "lobby_id": <str>,
            "game_mode": <str>,
            "max_players": <int>,
            "created_at": <str>
        }
    """
    return {
        "lobby_id": uuid.uuid4().hex[:8],
        "game_mode": game_mode,
        "max_players": max_players,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


@lob_mcp.tool()
def join_lobby(lobby_id: str, player: str) -> dict:
    """
    Add a player to an existing lobby.

    Parameters
    ----------
    lobby_id : str
        Identifier from `create_lobby`.
    player : str
        Username joining the lobby.

    Returns
    -------
    dict
        {
            "lobby_id": <str>,
            "player": <str>,
            "joined": <bool>
        }
    """
    return {"lobby_id": lobby_id, "player": player, "joined": True}


if __name__ == "__main__":
    lob_mcp.run(transport="stdio")
