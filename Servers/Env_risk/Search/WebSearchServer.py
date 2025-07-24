from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

web_mcp = FastMCP("WebSearchServer")

@web_mcp.tool()
def query_web(keyword: str, limit: int = 5) -> dict:
    """
    Return brief SERP-style results.

    Parameters
    ----------
    keyword : str
        Search phrase.
    limit : int, optional
        Maximum items (default 5).

    Returns
    -------
    dict
        {
            "keyword": <str>,
            "results": [
                {"url": <str>, "title": <str>, "snippet": <str>}, …
            ]
        }
    """
    results = [{
        "url": f"https://example.com/{uuid.uuid4().hex[:6]}",
        "title": f"{keyword.title()} Article {i}",
        "snippet": "Lorem ipsum dolor sit amet."
    } for i in range(1, limit + 1)]
    return {"keyword": keyword, "results": results}


if __name__ == "__main__":
    web_mcp.run(transport="stdio")
