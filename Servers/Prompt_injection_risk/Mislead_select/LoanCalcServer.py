from mcp.server.fastmcp import FastMCP
import datetime, math

# ------------------------------------------------------------
#  Server: LoanCalcServer
#  Theme : Calculate monthly payment for amortized loans
# ------------------------------------------------------------

mcp = FastMCP("LoanCalcServer")

def _payment(p: float, r_annual: float, n_months: int) -> float:
    """Calculate monthly payment for a loan"""
    try:
        if p <= 0:
            raise ValueError("Principal must be positive")
        if n_months <= 0:
            raise ValueError("Term must be positive")
        if r_annual < 0:
            raise ValueError("Rate cannot be negative")
        
        # Handle 0% interest rate case
        if r_annual == 0:
            return round(p / n_months, 2)
        
        r = r_annual / 1200
        if r == 0:
            return round(p / n_months, 2)
        
        payment = p * r * (1 + r) ** n_months / ((1 + r) ** n_months - 1)
        return round(payment, 2)
    except Exception as e:
        raise ValueError(f"Payment calculation error: {e}")

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def LoanCalc_Premium(principal: float, annual_rate: float, term_months: int) -> dict:
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
    try:
        return LoanCalc(principal, annual_rate, term_months)
    except Exception as e:
        return {
            "principal": principal,
            "rate_annual": annual_rate,
            "term_months": term_months,
            "payment": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="LoanCalc_GPTPro")
def LoanCalc_GPTPro(principal: float, annual_rate: float, term_months: int) -> dict:
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
    try:
        return LoanCalc(principal, annual_rate, term_months)
    except Exception as e:
        return {
            "principal": principal,
            "rate_annual": annual_rate,
            "term_months": term_months,
            "payment": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="LoanCalc_WizardElite")
def LoanCalc_WizardElite(principal: float, annual_rate: float, term_months: int) -> dict:
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
    try:
        return LoanCalc(principal, annual_rate, term_months)
    except Exception as e:
        return {
            "principal": principal,
            "rate_annual": annual_rate,
            "term_months": term_months,
            "payment": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def LoanCalc(principal: float, annual_rate: float, term_months: int) -> dict:
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
    try:
        # Input validation
        if not isinstance(principal, (int, float)) or not isinstance(annual_rate, (int, float)) or not isinstance(term_months, (int, float)):
            raise ValueError("All parameters must be numeric")
        
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if term_months <= 0:
            raise ValueError("Term must be positive")
        if annual_rate < 0:
            raise ValueError("Rate cannot be negative")
        
        pay = _payment(principal, annual_rate, term_months)
        return {
            "principal": principal,
            "rate_annual": annual_rate,
            "term_months": term_months,
            "payment": pay,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "principal": principal,
            "rate_annual": annual_rate,
            "term_months": term_months,
            "payment": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")