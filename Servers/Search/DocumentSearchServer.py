from mcp.server.fastmcp import FastMCP
import uuid, random

doc_mcp = FastMCP("DocumentSearchServer")

@doc_mcp.tool()
def find_documents(tags: list[str], limit: int = 5) -> dict:
    """
    Retrieve documents tagged with all specified keywords.

    Parameters
    ----------
    tags : list[str]
    limit : int, optional

    Returns
    -------
    dict
        {
            "tags": <list[str]>,
            "docs": [
                {"doc_id": <str>, "title": <str>}, …
            ]
        }
    """
    docs = [{"doc_id": uuid.uuid4().hex[:8], "title": f"Doc {i}"} for i in range(1, limit + 1)]
    return {"tags": tags, "docs": docs}


@doc_mcp.tool()
def doc_snippet(doc_id: str, length: int = 120) -> dict:
    """
    Fetch a preview snippet from a document.

    Parameters
    ----------
    doc_id : str
    length : int, optional

    Returns
    -------
    dict
        {"doc_id": <str>, "snippet": <str>}
    """
    snippet = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem."[:length]
    return {"doc_id": doc_id, "snippet": snippet}


if __name__ == "__main__":
    doc_mcp.run(transport="stdio")
