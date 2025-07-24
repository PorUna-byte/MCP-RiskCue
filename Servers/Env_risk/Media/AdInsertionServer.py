from mcp.server.fastmcp import FastMCP
import uuid, random

ad_mcp = FastMCP("AdInsertionServer")

@ad_mcp.tool()
def request_slot(asset_id: str, duration_sec: int) -> dict:
    """
    Reserve an ad slot within a stream.

    Parameters
    ----------
    asset_id : str
    duration_sec : int

    Returns
    -------
    dict
        {"slot_id": <str>, "approved": <bool>}
    """
    return {"slot_id": uuid.uuid4().hex, "approved": True}


@ad_mcp.tool()
def fill_slot(slot_id: str, ad_creative_url: str) -> dict:
    """
    Assign creative to a slot.

    Parameters
    ----------
    slot_id : str
    ad_creative_url : str

    Returns
    -------
    dict
        {"slot_id": <str>, "filled": <bool>}
    """
    return {"slot_id": slot_id, "filled": True}


if __name__ == "__main__":
    ad_mcp.run(transport="stdio")
