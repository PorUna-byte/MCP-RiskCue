from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

ref_mcp = FastMCP("RefundServer")

@ref_mcp.tool()
def request_refund(payment_id: str, amount: float, reason: str) -> dict:
    """
    Initiate a refund.

    Parameters
    ----------
    payment_id : str
    amount : float
    reason : str

    Returns
    -------
    dict
        {"refund_id": <str>, "submitted": <str>}
    """
    return {"refund_id": uuid.uuid4().hex, "submitted": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@ref_mcp.tool()
def refund_status(refund_id: str) -> dict:
    """
    Check progress of a refund.
    
    Parameters
    ----------
    refund_id : str
        Refund identifier (can be in various formats)
    
    Returns
    -------
    dict
        {"refund_id": <str>, "state": <str>} or error dict
    """
    # 如果refund_id为空，返回错误
    if not refund_id:
        return {
            "error": "No refund ID provided",
            "message": "Please provide a valid refund ID to check status"
        }
    
    # 直接在refund_id上进行正则化提取
    import re
    
    # 清理参数，移除引号和多余空格
    refund_id = refund_id.strip().strip('"\'')
    
    # 匹配多种表达方式
    patterns = [
        r'refund\s+(?:id\s+)?["\']?([^"\s]+)["\']?',
        r'refund\s+["\']?([^"\s]+)["\']?',
        r'#([^"\s]+)',  # 匹配 #rfnd_7890 格式
        r'([^"\s]+)',   # 通用匹配
    ]
    
    extracted_id = None
    for pattern in patterns:
        match = re.search(pattern, refund_id, re.IGNORECASE)
        if match:
            extracted_id = match.group(1)
            break
    
    # 如果没有匹配到，使用原始值
    if not extracted_id:
        extracted_id = refund_id
    
    # 验证refund_id格式
    if not re.match(r'^[a-zA-Z0-9\-_#]+$', extracted_id):
        return {
            "error": "Invalid refund ID format",
            "message": "Refund ID should contain only letters, numbers, hyphens, underscores, and hash symbols"
        }
    
    state = random.choice(["pending", "processed", "failed"])
    return {"refund_id": extracted_id, "state": state}


if __name__ == "__main__":
    ref_mcp.run(transport="stdio")
