from mcp.server.fastmcp import FastMCP
import uuid, random

mod_mcp = FastMCP("ModRepositoryServer")

@mod_mcp.tool()
def list_mods(game_id: str, limit: int = 5) -> dict:
    """
    Retrieve community mods for a game.

    Parameters
    ----------
    game_id : str
    limit : int, optional

    Returns
    -------
    dict
        {
            "mods": [
                {"mod_id": <str>, "title": <str>, "downloads": <int>}, …
            ]
        }
    """
    mods = [{
        "mod_id": uuid.uuid4().hex[:8],
        "title": f"Cool Mod {i}",
        "downloads": random.randint(1000, 50000)
    } for i in range(limit)]
    return {"mods": mods}


@mod_mcp.tool()
def download_mod(mod_id: str) -> dict:
    """
    Provide a secure download link.

    Parameters
    ----------
    mod_id : str

    Returns
    -------
    dict
        {
            "mod_id": <str>,
            "url": <str>
        }
    """
    return {"mod_id": mod_id, "url": f"https://mods.example.com/{mod_id}.zip"}


if __name__ == "__main__":
    mod_mcp.run(transport="stdio")
