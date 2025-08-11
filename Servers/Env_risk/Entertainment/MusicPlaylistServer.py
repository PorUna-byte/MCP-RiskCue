from mcp.server.fastmcp import FastMCP
import uuid, random

music_mcp = FastMCP("MusicPlaylistServer")

# 存储playlist信息的简单内存存储
playlist_store = {}

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
    playlist_id = f"{user_id}_{name}_{uuid.uuid4().hex[:8]}"
    playlist_store[playlist_id] = {"user_id": user_id, "name": name, "tracks": []}
    return {"playlist_id": playlist_id, "name": name}


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
    if playlist_id in playlist_store:
        playlist_store[playlist_id]["tracks"].append(track_id)
        return {"playlist_id": playlist_id, "track_id": track_id, "added": True}
    else:
        return {"playlist_id": playlist_id, "track_id": track_id, "added": False}


@music_mcp.tool()
def get_playlist(playlist_id: str, user_id: str = "default_user") -> dict:
    """
    Retrieve current playlist contents.

    Parameters
    ----------
    playlist_id : str
        Playlist identifier.
    user_id : str, optional
        User identifier (default: "default_user").

    Returns
    -------
    dict
        {
            "playlist_id": <str>,
            "tracks": [<str>, …]   # list of track IDs
        }
    """
    # 如果playlist_id是playlist名称而不是完整ID，尝试查找
    if playlist_id not in playlist_store:
        # 尝试通过名称查找
        for pid, info in playlist_store.items():
            if info["name"] == playlist_id:
                playlist_id = pid
                break
        else:
            # 如果找不到，创建默认playlist
            playlist_id = f"{user_id}_{playlist_id}_{uuid.uuid4().hex[:8]}"
            playlist_store[playlist_id] = {"user_id": user_id, "name": playlist_id, "tracks": []}
    
    tracks = playlist_store[playlist_id]["tracks"]
    if not tracks:
        # 如果没有tracks，生成一些示例tracks
        tracks = [f"TRK{random.randint(1000, 9999)}" for _ in range(random.randint(3, 10))]
        playlist_store[playlist_id]["tracks"] = tracks
    
    return {"playlist_id": playlist_id, "tracks": tracks}


if __name__ == "__main__":
    music_mcp.run(transport="stdio")
