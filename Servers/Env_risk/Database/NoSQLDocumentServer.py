from mcp.server.fastmcp import FastMCP
import uuid
import random
from typing import Any

doc_mcp = FastMCP("NoSQLDocumentServer")

@doc_mcp.tool()
def insert(collection: str, document_json: dict) -> dict:
    """
    Insert a JSON document into a collection.

    Parameters
    ----------
    collection : str
        Target collection name (e.g., `"users"`).
    document_json : dict
        JSON dictionary representing the document to store.

    Returns
    -------
    dict
        {
            "document_id": <str>,  
            "collection":  <str>, 
        }
    """

    return {"document_id": uuid.uuid4().hex, "collection": collection}

@doc_mcp.tool()
def find(collection: str, filter_json: dict, limit: int = 5) -> dict:
    """
    Retrieve up to *limit* documents that satisfy the given JSON filter.

    Parameters
    ----------
    collection : str
        Collection to query.
    filter_json : dict
        JSON-dictionary specification (e.g., `'{"status": "active"}'`).
    limit : int, optional
        Maximum number of documents to return (default 5).

    Returns
    -------
    dict
        {
            "collection": <str>, 
            "documents":  [ 
                "_id": <str>,
                ...
            ]
        }
    """
    docs = [{"_id": uuid.uuid4().hex} for _ in range(limit)]
    return {"collection": collection, "documents": docs}


if __name__ == "__main__":
    doc_mcp.run(transport="stdio")

