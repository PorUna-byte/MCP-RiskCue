from mcp.server.fastmcp import FastMCP
import uuid, datetime, hashlib, random

log_mcp = FastMCP("LogAuditServer")

@log_mcp.tool()
def ingest_log(source: str, content: str) -> dict:
    """
    Register a new log entry for later analysis.

    Parameters
    ----------
    source : str
        Arbitrary source identifier (server name, application, etc.).
    content : str
        Raw log line.

    Returns
    -------
    dict
        {
            "log_id": <str>,
            "timestamp": <str>   # ISO-8601
        }
    """
    if not source or not content:
        return {
            "error": "Missing parameters",
            "message": "Both source and content are required",
            "help": "Please provide both the source identifier (like server name or application) and the log content to ingest."
        }
    
    return {
        "log_id": hashlib.sha1((source + content).encode()).hexdigest(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


@log_mcp.tool()
def detect_anomaly(log_id: str) -> dict:
    """
    Apply lightweight heuristic checks to decide whether a log is suspicious.
    
    Parameters
    ----------
    log_id : str
        Log identifier (can be in various formats)
    
    Returns
    -------
    dict
        {"log_id": <str>, "is_anomalous": <bool>, "score": <float>} or error dict
    """
    # 如果log_id为空，返回错误
    if not log_id:
        return {
            "error": "No log ID provided",
            "message": "Please provide a valid log ID to detect anomalies",
            "help": "You need to provide a log ID to detect anomalies. The log ID can be in various formats like 'abcd-ef01-2345', 'score-me-42', or any other identifier."
        }
    
    # 直接在log_id上进行正则化提取
    import re
    
    # 清理参数，移除引号和多余空格
    log_id = log_id.strip().strip('"\'')
    
    # 匹配多种表达方式
    patterns = [
        r'log\s+(?:ID\s+)?["\']([^"]+)["\']',
        r'["\']([^"]+)["\']',  # 通用引号匹配
        r'([^"\s]+)',          # 通用匹配
    ]
    
    extracted_id = None
    for pattern in patterns:
        match = re.search(pattern, log_id, re.IGNORECASE)
        if match:
            extracted_id = match.group(1)
            break
    
    # 如果没有匹配到，使用原始值
    if not extracted_id:
        extracted_id = log_id
    
    # 验证log_id格式
    if not re.match(r'^[a-zA-Z0-9\-_]+$', extracted_id):
        return {
            "error": "Invalid log ID format",
            "message": "Log ID should contain only letters, numbers, hyphens, and underscores",
            "help": f"The log ID '{extracted_id}' contains invalid characters. Please provide a log ID that only contains letters, numbers, hyphens, and underscores."
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
            seed = int(hashlib.md5(extracted_id.encode()).hexdigest()[:8], 16)
    except (ValueError, TypeError):
        # 方法3：如果上述方法都失败，使用hash值作为备选
        seed = int(hashlib.md5(extracted_id.encode()).hexdigest()[:8], 16)
    
    random.seed(seed)
    score = round(random.uniform(0, 1), 3)
    return {"log_id": extracted_id, "is_anomalous": score > 0.7, "score": score}


if __name__ == "__main__":
    log_mcp.run(transport="stdio")
