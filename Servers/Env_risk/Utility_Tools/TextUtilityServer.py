from mcp.server.fastmcp import FastMCP

txt_mcp = FastMCP("TextUtilityServer")


@txt_mcp.tool()
def char_count(text: str) -> dict:
    """
    Count characters and words in a string.

    Parameters
    ----------
    text : str
        Input text.

    Returns
    -------
    dict
        {"chars": <int>, "words": <int>}
    """
    chars = len(text)
    words = len(text.split())
    return {"chars": chars, "words": words}


@txt_mcp.tool()
def to_snake_case(raw: str) -> dict:
    """
    Convert a phrase to snake_case.

    Parameters
    ----------
    raw : str
        Original phrase.

    Returns
    -------
    dict
        {"original": <str>, "snake": <str>}
    """
    snake = "_".join(raw.lower().split())
    return {"original": raw, "snake": snake}


if __name__ == "__main__":
    txt_mcp.run(transport="stdio")
