from mcp.server.fastmcp import FastMCP
import uuid

gro_mcp = FastMCP("GroceryListServer")

@gro_mcp.tool()
def create_list(user_id: str, title: str) -> dict:
    """
    Start an empty grocery list.

    Parameters
    ----------
    user_id : str
    title : str

    Returns
    -------
    dict
        {
            "list_id": <str>,
            "title": <str>
        }
    """
    return {"list_id": uuid.uuid4().hex, "title": title}


@gro_mcp.tool()
def add_item(list_id: str, item: str, qty: str = "1") -> dict:
    """
    Append an item to a grocery list.

    Parameters
    ----------
    list_id : str
    item : str
    qty : str, optional
        Quantity descriptor (default '1').

    Returns
    -------
    dict
        {
            "list_id": <str>,
            "item": <str>,
            "qty": <str>
        }
    """
    return {"list_id": list_id, "item": item, "qty": qty}


if __name__ == "__main__":
    gro_mcp.run(transport="stdio")
