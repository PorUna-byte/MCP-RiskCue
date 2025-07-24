from mcp.server.fastmcp import FastMCP
import random
import uuid

rnd_mcp = FastMCP("RandomDataServer")

@rnd_mcp.tool()
def random_string(length: int = 8) -> dict:
    """
    Generate an alphanumeric random string.

    Parameters
    ----------
    length : int, optional
        Desired string length (default 8).

    Returns
    -------
    dict
        {"length": <int>, "value": <str>}
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    value = "".join(random.choice(chars) for _ in range(length))
    return {"length": length, "value": value}


@rnd_mcp.tool()
def uuid_v4() -> dict:
    """
    Produce a UUIDv4 value.

    Returns
    -------
    dict
        {"uuid": <str>}
    """
    return {"uuid": str(uuid.uuid4())}


if __name__ == "__main__":
    rnd_mcp.run(transport="stdio")
