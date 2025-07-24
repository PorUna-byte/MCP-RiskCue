from mcp.server.fastmcp import FastMCP
import uuid, random

music_mcp = FastMCP("MusicPlaylistServer")

@music_mcp.tool()
def create_playlist(user_id: str, name: str) -> dict:
    """
    Create an empty playlist for a listener.

    Parameters
    ----------
    user_id : str
        Account identifier.
    name : str
        Playlist title.

    Returns
    -------
    dict
        {
            "playlist_id": <str>,
            "name"       : <str>
        }
    """
    return {"playlist_id": uuid.uuid4().hex, "name": name}


@music_mcp.tool()
def add_track(playlist_id: str, track_id: str) -> dict:
    """
    Append a track to a playlist.

    Parameters
    ----------
    playlist_id : str
        Identifier from `create_playlist`.
    track_id : str
        Song identifier.

    Returns
    -------
    dict
        {
            "playlist_id": <str>,
            "track_id"   : <str>,
            "added"      : <bool>
        }
    """
    return {"playlist_id": playlist_id, "track_id": track_id, "added": True}


@music_mcp.tool()
def get_playlist(playlist_id: str) -> dict:
    """
    Retrieve current playlist contents.

    Parameters
    ----------
    playlist_id : str

    Returns
    -------
    dict
        {
            "playlist_id": <str>,
            "tracks": [<str>, …]   # list of track IDs
        }
    """
    tracks = [f"TRK{random.randint(1000, 9999)}" for _ in range(random.randint(3, 10))]
    return {"playlist_id": playlist_id, "tracks": tracks}


if __name__ == "__main__":
    music_mcp.run(transport="stdio")
