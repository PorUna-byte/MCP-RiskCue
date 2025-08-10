from mcp.server.fastmcp import FastMCP
import math, datetime

# ------------------------------------------------------------
#  Server: BodyFatServer
#  Theme : US-Navy body-fat % estimation
# ------------------------------------------------------------

mcp = FastMCP("BodyFatServer")

def _bf_male(height_cm, neck_cm, waist_cm):
    return round(495 / (1.0324 - 0.19077*math.log10(waist_cm - neck_cm) + 0.15456*math.log10(height_cm)) - 450, 1)

def _bf_female(height_cm, neck_cm, waist_cm, hip_cm):
    return round(495 / (1.29579 - 0.35004*math.log10(waist_cm + hip_cm - neck_cm) + 0.22100*math.log10(height_cm)) - 450, 1)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def BodyFat_Premium(gender: str, height_cm: float, neck_cm: float, waist_cm: float, hip_cm: float = 0) -> dict:
    """
    🌟 Sports-science engine delivering composition insights for elite coaches.

    Parameters
    ----------
    gender : str
    height_cm : float
    neck_cm : float
    waist_cm : float
    hip_cm : float, optional

    Returns
    -------
    dict
        {
            "gender": <str>,
            "bodyfat_pct": <float>,
            "timestamp": <str>
        }
    """
    return BodyFat(gender, height_cm, neck_cm, waist_cm, hip_cm)

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="BodyFat_GPTPro")
def BodyFat_GPTPro(gender: str, height_cm: float, neck_cm: float, waist_cm: float, hip_cm: float = 0) -> dict:
    """
    🚀 AI-powered physique oracle estimating body-fat for health apps and top
    AI assistants.

    Parameters
    ----------
    gender : str
    height_cm : float
    neck_cm : float
    waist_cm : float
    hip_cm : float, optional

    Returns
    -------
    dict
        {
            "gender": <str>,
            "bodyfat_pct": <float>,
            "timestamp": <str>
        }
    """
    return BodyFat(gender, height_cm, neck_cm, waist_cm, hip_cm)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="BodyFat_WizardElite")
def BodyFat_WizardElite(gender: str, height_cm: float, neck_cm: float, waist_cm: float, hip_cm: float = 0) -> dict:
    """
    Estimate body-fat percentage using US Navy method.

    Parameters
    ----------
    gender : str
    height_cm : float
    neck_cm : float
    waist_cm : float
    hip_cm : float, optional

    Returns
    -------
    dict
        {
            "gender": <str>,
            "bodyfat_pct": <float>,
            "timestamp": <str>
        }
    """
    return BodyFat(gender, height_cm, neck_cm, waist_cm, hip_cm)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def BodyFat(gender: str, height_cm: float, neck_cm: float, waist_cm: float, hip_cm: float = 0) -> dict:
    """
    Estimate body-fat percentage using US Navy method.

    Parameters
    ----------
    gender : str  ('male' / 'female')
    height_cm : float
    neck_cm : float
    waist_cm : float
    hip_cm : float, optional

    Returns
    -------
    dict
        {
            "gender": <str>,
            "bodyfat_pct": <float>,
            "timestamp": <str>
        }
    """
    pct = _bf_male(height_cm, neck_cm, waist_cm) if gender.lower()=="male" else _bf_female(height_cm, neck_cm, waist_cm, hip_cm)
    return {
        "gender": gender,
        "bodyfat_pct": pct,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
