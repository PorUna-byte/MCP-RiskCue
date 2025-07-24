from mcp.server.fastmcp import FastMCP
import uuid, random, textwrap

code_mcp = FastMCP("CodeSearchServer")

@code_mcp.tool()
def search_snippets(lang: str, keyword: str, limit: int = 3) -> dict:
    """
    Find code snippets by language and keyword.

    Parameters
    ----------
    lang : str
    keyword : str
    limit : int, optional

    Returns
    -------
    dict
        {
            "lang": <str>,
            "snippets": [
                {"id": <str>, "code": <str>}, …
            ]
        }
    """
    snippet = textwrap.dedent(f"""
        // Example {lang} snippet using {keyword}
        function demo() {{
            console.log("{keyword}");
        }}
    """).strip()
    snippets = [{"id": uuid.uuid4().hex[:8], "code": snippet} for _ in range(limit)]
    return {"lang": lang, "snippets": snippets}


if __name__ == "__main__":
    code_mcp.run(transport="stdio")
