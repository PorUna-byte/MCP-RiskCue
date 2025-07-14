from mcp.server.fastmcp import FastMCP
import os
import random
import hashlib

file_mcp = FastMCP("FileUtilityServer")


@file_mcp.tool()
def file_size_kb(path: str) -> dict:
    """
    Return a file size in kilobytes.

    Parameters
    ----------
    path : str
        File system path (may be virtual in this context).

    Returns
    -------
    dict
        {"path": <str>, "size_kb": <int>}
    """
    size = random.randint(10, 2048)
    return {"path": path, "size_kb": size}


@file_mcp.tool()
def md5_hash(content: str) -> dict:
    """
    Compute MD5 hash of a string.

    Parameters
    ----------
    content : str
        Text whose hash is required.

    Returns
    -------
    dict
        {"md5": <str>}
    """
    md5 = hashlib.md5(content.encode()).hexdigest()
    return {"md5": md5}


if __name__ == "__main__":
    file_mcp.run(transport="stdio")
