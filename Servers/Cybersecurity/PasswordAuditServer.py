from mcp.server.fastmcp import FastMCP
import string, datetime

pwd_mcp = FastMCP("PasswordAuditServer")

@pwd_mcp.tool()
def evaluate_strength(password: str) -> dict:
    """
    Score the strength of a password.

    Parameters
    ----------
    password : str
        Plain-text password.

    Returns
    -------
    dict
        {
            "score": <int>,          
            "diversity": <int>,    
            "crack_time_estimate": <str>,
            "timestamp": <str ISO-8601>
        }
    """
    # 1) 长度得分：每字符 4 分，上限 40 分
    length_score = min(len(password) * 4, 40)

    # 2) 字符类别多样性（共 4 类）
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_punct = any(c in string.punctuation for c in password)
    diversity = sum([has_lower, has_upper, has_digit, has_punct])   # 0–4

    # 3) 综合得分
    score = min(length_score + diversity * 15, 100)

    # 4) 粗略破解时间估计
    crack_time_estimate = (
        "years"   if score > 85 else
        "months"  if score > 60 else
        "days"    if score > 40 else
        "hours"
    )

    return {
        "score": score,
        "diversity": diversity,
        "crack_time_estimate": crack_time_estimate,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    pwd_mcp.run(transport="stdio")

