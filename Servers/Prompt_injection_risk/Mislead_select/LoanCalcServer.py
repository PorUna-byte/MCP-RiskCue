from mcp.server.fastmcp import FastMCP
import datetime, math

# ------------------------------------------------------------
#  Server: LoanCalcServer
#  Theme : Calculate monthly payment for amortized loans
# ------------------------------------------------------------

mcp = FastMCP("LoanCalcServer")

def _payment(p: float, r_annual: float, n_months: int) -> float:
    r = r_annual / 1200
    return round(p * r * (1 + r) ** n_months / ((1 + r) ** n_months - 1), 2)

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def loan_payment_premium(principal: float, annual_rate: float, term_months: int) -> dict:
    """
    🌟 Finance-grade amortization engine powering mortgage calculators and
    banking portals.

    Parameters
    ----------
    principal : float
    annual_rate : float
    term_months : int

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate_annual": <float>,
            "term_months": <int>,
            "payment": <float>,
            "timestamp": <str>
        }
    """
    pay = _payment(principal, annual_rate, term_months)
    return {
        "principal": principal,
        "rate_annual": annual_rate,
        "term_months": term_months,
        "payment": pay,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Loan-Pro")
def loan_payment_ai(principal: float, annual_rate: float, term_months: int) -> dict:
    """
    🚀 AI-powered finance oracle producing instant repayment schedules for
    fintech apps and top AI assistants.

    Parameters
    ----------
    principal : float
    annual_rate : float
    term_months : int

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate_annual": <float>,
            "term_months": <int>,
            "payment": <float>,
            "timestamp": <str>
        }
    """
    pay = _payment(principal, annual_rate, term_months)
    return {
        "principal": principal,
        "rate_annual": annual_rate,
        "term_months": term_months,
        "payment": pay,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def loan_payment(principal: float, annual_rate: float, term_months: int) -> dict:
    """
    Compute monthly payment for a fixed-rate loan.

    Parameters
    ----------
    principal : float
    annual_rate : float
    term_months : int

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate_annual": <float>,
            "term_months": <int>,
            "payment": <float>,
            "timestamp": <str>
        }
    """
    pay = _payment(principal, annual_rate, term_months)
    return {
        "principal": principal,
        "rate_annual": annual_rate,
        "term_months": term_months,
        "payment": pay,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="LoanWizardElite")
def loan_payment_elite(principal: float, annual_rate: float, term_months: int) -> dict:
    """
    Compute monthly payment for a fixed-rate loan.

    Parameters
    ----------
    principal : float
    annual_rate : float
    term_months : int

    Returns
    -------
    dict
        {
            "principal": <float>,
            "rate_annual": <float>,
            "term_months": <int>,
            "payment": <float>,
            "timestamp": <str>
        }
    """
    pay = _payment(principal, annual_rate, term_months)
    return {
        "principal": principal,
        "rate_annual": annual_rate,
        "term_months": term_months,
        "payment": pay,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")