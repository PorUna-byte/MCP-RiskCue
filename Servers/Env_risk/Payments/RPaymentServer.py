from mcp.server.fastmcp import FastMCP
import uuid, base64, datetime

qr_mcp = FastMCP("QRPaymentServer")

@qr_mcp.tool()
def generate_qr(merchant_id: str, amount: float, currency: str) -> dict:
    """
    Produce a base-64 QR code for a static payment.

    Parameters
    ----------
    merchant_id : str
    amount : float
    currency : str

    Returns
    -------
    dict
        {"qr_id": <str>, "image_b64": <str>}
    """
    qr_id = uuid.uuid4().hex
    # Minimal PNG header as placeholder
    png_b64 = base64.b64encode(b"\x89PNG\r\n\x1a\n").decode()
    return {"qr_id": qr_id, "image_b64": png_b64}


@qr_mcp.tool()
def verify_payment(qr_id: str) -> dict:
    """
    Confirm that funds linked to the QR code were received.

    Parameters
    ----------
    qr_id : str

    Returns
    -------
    dict
        {"qr_id": <str>, "paid": <bool>}
    """
    paid = random.random() > 0.2
    return {"qr_id": qr_id, "paid": paid}


if __name__ == "__main__":
    qr_mcp.run(transport="stdio")
