from mcp.server.fastmcp import FastMCP
import uuid, base64, datetime, random

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
        QR code identifier (can be in various formats)
    
    Returns
    -------
    dict
        {"qr_id": <str>, "paid": <bool>} or error dict
    """
    # 如果qr_id为空，返回错误
    if not qr_id:
        return {
            "error": "No QR ID provided",
            "message": "Please provide a valid QR ID to check payment status"
        }
    
    # 直接在qr_id上进行正则化提取
    import re
    
    # 清理参数，移除引号和多余空格
    qr_id = qr_id.strip().strip('"\'')
    
    # 匹配多种表达方式
    patterns = [
        r'QR\s+(?:ID\s+)?["\']([^"]+)["\']',
        r'QR\s+code\s+["\']([^"]+)["\']',
        r'["\']([^"]+)["\']',  # 通用引号匹配
        r'([^"\s]+)',          # 通用匹配
    ]
    
    extracted_id = None
    for pattern in patterns:
        match = re.search(pattern, qr_id, re.IGNORECASE)
        if match:
            extracted_id = match.group(1)
            break
    
    # 如果没有匹配到，使用原始值
    if not extracted_id:
        extracted_id = qr_id
    
    # 验证qr_id格式
    if len(extracted_id) < 1 or len(extracted_id) > 100:
        return {
            "error": "Invalid QR ID length",
            "message": "QR ID should be between 1 and 100 characters"
        }
    
    paid = random.random() > 0.2
    return {"qr_id": extracted_id, "paid": paid}


if __name__ == "__main__":
    qr_mcp.run(transport="stdio")
