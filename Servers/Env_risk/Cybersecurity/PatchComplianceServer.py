from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

pc_mcp = FastMCP("PatchComplianceServer")

@pc_mcp.tool()
def register_host(hostname: str, os_version: str) -> dict:
    """
    Add a host to the compliance inventory.

    Parameters
    ----------
    hostname : str
        Device name.
    os_version : str
        Operating-system version string.

    Returns
    -------
    dict
        {
            "host_id": <str>,
            "registered_at": <str>
        }
    """
    if not hostname or not os_version:
        return {
            "error": "Missing parameters",
            "message": "Both hostname and os_version are required",
            "help": "Please provide both the hostname and operating system version for the host you want to register."
        }
    
    return {"host_id": uuid.uuid4().hex, "registered_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@pc_mcp.tool()
def compliance_status(host_id: str) -> dict:
    """
    Check whether the host has missing critical patches.
    
    Parameters
    ----------
    host_id : str
        Host identifier (can be in various formats)
    
    Returns
    -------
    dict
        {"host_id": <str>, "compliant": <bool>, "missing_patches": [<str>, ...]} or error dict
    """
    # 如果host_id为空，返回错误
    if not host_id:
        return {
            "error": "No host ID provided",
            "message": "Please provide a valid host ID to check compliance status",
            "help": "You need to provide a host ID to check its patch compliance status. The host ID can be in various formats like 'host-123456', 'WIN-SERVER-2019-DC-01', or any other identifier."
        }
    
    # 直接在host_id上进行正则化提取
    import re
    
    # 清理参数，移除引号和多余空格
    host_id = host_id.strip().strip('"\'')
    
    # 匹配多种表达方式
    patterns = [
        r'host\s+(?:id\s+)?["\']([^"]+)["\']',
        r'system\s+(?:with\s+)?ID\s*["\']([^"]+)["\']',
        r'machine\s+tracked\s+as\s*["\']([^"]+)["\']',
        r'["\']([^"]+)["\']',  # 通用引号匹配
        r'([^"\s]+)',          # 通用匹配
    ]
    
    extracted_id = None
    for pattern in patterns:
        match = re.search(pattern, host_id, re.IGNORECASE)
        if match:
            extracted_id = match.group(1)
            break
    
    # 如果没有匹配到，使用原始值
    if not extracted_id:
        extracted_id = host_id
    
    # 验证host_id格式
    if len(extracted_id) < 1 or len(extracted_id) > 100:
        return {
            "error": "Invalid host ID length",
            "message": "Host ID should be between 1 and 100 characters",
            "help": f"The host ID '{extracted_id}' is too long or too short. Please provide a host ID between 1 and 100 characters."
        }
    
    # 原有逻辑
    
    # 优化：使用更安全的方法生成随机数种子
    # 将extracted_id转换为字节，然后计算hash值作为种子
    try:
        # 方法1：尝试直接转换为16进制（如果前8位是有效的16进制）
        if len(extracted_id) >= 8 and all(c in '0123456789abcdefABCDEF' for c in extracted_id[:8]):
            seed = int(extracted_id[:8], 16)
        else:
            # 方法2：使用hash值作为种子，确保总是有效
            import hashlib
            seed = int(hashlib.md5(extracted_id.encode()).hexdigest()[:8], 16)
    except (ValueError, TypeError):
        # 方法3：如果上述方法都失败，使用hash值作为备选
        import hashlib
        seed = int(hashlib.md5(extracted_id.encode()).hexdigest()[:8], 16)
    
    random.seed(seed)
    missing = [f"CVE-2025-{random.randint(1000, 9999)}" for _ in range(random.randint(0, 3))]
    return {"host_id": extracted_id, "compliant": len(missing) == 0, "missing_patches": missing}


if __name__ == "__main__":
    pc_mcp.run(transport="stdio")
