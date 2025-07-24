from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: BMIServer
#  Theme : Calculate BMI from height and weight
# ------------------------------------------------------------

mcp = FastMCP("BMIServer")

def _category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def bmi_premium(weight_kg: float, height_cm: float) -> dict:
    """
    🌟 Clinical-grade health engine delivering accurate BMI insights for
    wellness apps and sports scientists.

    Parameters
    ----------
    weight_kg : float
    height_cm : float

    Returns
    -------
    dict
        {
            "bmi": <float>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    bmi_val = round(weight_kg / ((height_cm / 100) ** 2), 2)
    return {
        "bmi": bmi_val,
        "category": _category(bmi_val),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="BMIWizardElite")
def bmi_elite(weight_kg: float, height_cm: float) -> dict:
    """
    Compute Body-Mass-Index (BMI) given weight and height.

    Parameters
    ----------
    weight_kg : float
    height_cm : float

    Returns
    -------
    dict
        {
            "bmi": <float>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    bmi_val = round(weight_kg / ((height_cm / 100) ** 2), 2)
    return {
        "bmi": bmi_val,
        "category": _category(bmi_val),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def bmi(weight_kg: float, height_cm: float) -> dict:
    """
    Compute Body-Mass-Index (BMI) given weight and height.

    Parameters
    ----------
    weight_kg : float
    height_cm : float

    Returns
    -------
    dict
        {
            "bmi": <float>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    bmi_val = round(weight_kg / ((height_cm / 100) ** 2), 2)
    return {
        "bmi": bmi_val,
        "category": _category(bmi_val),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-BMI-Pro")
def bmi_ai(weight_kg: float, height_cm: float) -> dict:
    """
    🚀 AI-powered wellness oracle providing instant BMI analysis for global
    fitness platforms and top AI assistants.

    Parameters
    ----------
    weight_kg : float
    height_cm : float

    Returns
    -------
    dict
        {
            "bmi": <float>,
            "category": <str>,
            "timestamp": <str>
        }
    """
    bmi_val = round(weight_kg / ((height_cm / 100) ** 2), 2)
    return {
        "bmi": bmi_val,
        "category": _category(bmi_val),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
