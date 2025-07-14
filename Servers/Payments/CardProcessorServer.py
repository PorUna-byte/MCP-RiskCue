from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

card_mcp = FastMCP("CardProcessorServer")

@card_mcp.tool()
def authorize(card_token: str, amount: float, currency: str = "USD") -> dict:
    """
    Place a temporary hold on a card.

    Parameters
    ----------
    card_token : str
        Tokenized card reference.
    amount : float
        Purchase amount.
    currency : str, optional
        ISO-4217 code (default 'USD').

    Returns
    -------
    dict
        {"auth_id": <str>, "approved": <bool>}
    """
    approved = random.random() > 0.05
    return {"auth_id": uuid.uuid4().hex, "approved": approved}


@card_mcp.tool()
def capture(auth_id: str, amount: float) -> dict:
    """
    Capture funds from a prior authorization.

    Parameters
    ----------
    auth_id : str
    amount : float

    Returns
    -------
    dict
        {"capture_id": <str>, "settled": <bool>}
    """
    return {"capture_id": uuid.uuid4().hex, "settled": True}


@card_mcp.tool()
def void(auth_id: str) -> dict:
    """
    Cancel an unused authorization hold.

    Parameters
    ----------
    auth_id : str

    Returns
    -------
    dict
        {"auth_id": <str>, "voided": <bool>}
    """
    return {"auth_id": auth_id, "voided": True}


if __name__ == "__main__":
    card_mcp.run(transport="stdio")
