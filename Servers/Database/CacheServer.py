from mcp.server.fastmcp import FastMCP
import datetime
import hashlib

cache_mcp = FastMCP("CacheServer")

@cache_mcp.tool()
def set_key(key: str, value: str, ttl_seconds: int = 300) -> dict:
    """
    Store a key–value pair in the cache with a time-to-live (TTL).

    Parameters
    ----------
    key : str
        Cache key (unique identifier).
    value : str
        String data to be stored.
    ttl_seconds : int, optional
        Time-to-live in seconds (default 300 s).

    Returns
    -------
    dict
        {
            "stored":      <bool>, 
            "expires_at":  <str>,
        }
    """
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=ttl_seconds)
    return {"stored": True, "expires_at": exp.isoformat() + "Z"}


@cache_mcp.tool()
def get_key(key: str) -> dict:
    """
    Fetch a value from the cache.

    Parameters
    ----------
    key : str
        Cache key to look up.

    Returns
    -------
    dict
        {
            "found": <bool>,
            "value": <str>, 
        }
    """
    hashed = hashlib.sha256(key.encode()).hexdigest()
    return {"found": True, "value": f"cached_value_{hashed[:8]}"}


if __name__ == "__main__":
    cache_mcp.run(transport="stdio")

