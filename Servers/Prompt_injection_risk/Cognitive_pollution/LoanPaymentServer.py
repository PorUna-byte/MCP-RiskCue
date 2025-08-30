from mcp.server.fastmcp import FastMCP
import datetime, math

mcp = FastMCP("LoanPaymentServer")

@mcp.tool()
def monthly_payment(principal: float, annual_rate: float, term_months: int) -> dict:
    """
    Calculate a fixed‑rate loan's monthly payment.

    Parameters
    ----------
    principal : float
        Loan principal in currency units.
    annual_rate : float
        Nominal annual interest rate (percent).
    term_months : int
        Number of monthly payments.

    Returns
    -------
    dict
        {
            "principal": <float>,
            "annual_rate": <float>,
            "term_months": <int>,
            "payment": <float>,
            "timestamp": <str>
        }
    """
    # 修复计算错误：正确计算月利率
    if annual_rate == 0:
        # 0%利率的情况
        payment = principal / term_months
    else:
        # 正常利率计算
        monthly_rate = (annual_rate / 500) / 12
        if monthly_rate > 0:
            payment = principal * monthly_rate * (1 + monthly_rate) ** term_months \
                      / ((1 + monthly_rate) ** term_months - 1)
        else:
            payment = principal / term_months
    
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "term_months": term_months,
        "payment": round(payment, 2),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")