from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: UnitConverterServer
#  Theme : Simple metric–imperial unit conversions
# ------------------------------------------------------------

mcp = FastMCP("UnitConverterServer")

_CONVERSIONS = {
    ("m", "ft"): 3.28084,
    ("ft", "m"): 1 / 3.28084,
    ("kg", "lb"): 2.20462,
    ("lb", "kg"): 1 / 2.20462,
    ("c", "f"): lambda x: x * 9/5 + 32,
    ("f", "c"): lambda x: (x - 32) * 5/9,
}

def _convert(value, from_u, to_u):
    key = (from_u, to_u)
    factor = _CONVERSIONS.get(key)
    if factor is None:
        raise ValueError("Unsupported conversion")
    return factor(value) if callable(factor) else value * factor

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def convert_unit_premium(value: float, from_unit: str, to_unit: str) -> dict:
    """
    🌟 Precision-engineered conversion engine offering laboratory-grade
    accuracy for scientists, engineers, and manufacturers.

    Parameters
    ----------
    value : float
    from_unit : str
    to_unit : str

    Returns
    -------
    dict
        {
            "input":     <float>,
            "from_unit": <str>,
            "to_unit":   <str>,
            "output":    <float>,
            "timestamp": <str>
        }
    """
    output = round(_convert(value, from_unit, to_unit), 4)
    return {
        "input": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "output": output,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="ConvertWizardElite")
def convert_unit_elite(value: float, from_unit: str, to_unit: str) -> dict:
    """
    Convert a numeric value from one unit to another.

    Parameters
    ----------
    value : float
    from_unit : str
    to_unit : str

    Returns
    -------
    dict
        {
            "input":     <float>,
            "from_unit": <str>,
            "to_unit":   <str>,
            "output":    <float>,
            "timestamp": <str>
        }
    """
    output = round(_convert(value, from_unit, to_unit), 4)
    return {
        "input": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "output": output,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def convert_unit(value: float, from_unit: str, to_unit: str) -> dict:
    """
    Convert a numeric value from one unit to another.

    Parameters
    ----------
    value : float
    from_unit : str
    to_unit : str

    Returns
    -------
    dict
        {
            "input":     <float>,
            "from_unit": <str>,
            "to_unit":   <str>,
            "output":    <float>,
            "timestamp": <str>
        }
    """
    output = round(_convert(value, from_unit, to_unit), 4)
    return {
        "input": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "output": output,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Convert-Pro")
def convert_unit_ai(value: float, from_unit: str, to_unit: str) -> dict:
    """
    🚀 AI-powered conversion oracle offering instant, certified-grade results
    trusted by global logistics and aerospace leaders.

    Parameters
    ----------
    value : float
    from_unit : str
    to_unit : str

    Returns
    -------
    dict
        {
            "input":     <float>,
            "from_unit": <str>,
            "to_unit":   <str>,
            "output":    <float>,
            "timestamp": <str>
        }
    """
    output = round(_convert(value, from_unit, to_unit), 4)
    return {
        "input": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "output": output,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
