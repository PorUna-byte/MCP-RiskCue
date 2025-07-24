from mcp.server.fastmcp import FastMCP
import secrets, base64

rand_mcp = FastMCP("RandomnessServer")

@rand_mcp.tool()
def generate_secure_random_bytes(length: int = 32) -> dict:
    """
    Produce cryptographically strong random bytes.

    Parameters
    ----------
    length : int, optional
        Number of random bytes requested (default 32).

    Returns
    -------
    dict
        {
            "random_b64": <str>
        }
    """
    rand = secrets.token_bytes(length)
    return {"random_b64": base64.b64encode(rand).decode()}


if __name__ == "__main__":
    rand_mcp.run(transport="stdio")
