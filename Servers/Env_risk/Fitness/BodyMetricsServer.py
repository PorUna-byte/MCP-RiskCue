from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

body_mcp = FastMCP("BodyMetricsServer")

@body_mcp.tool()
def record_measurement(user_id: str, weight_kg: float, body_fat_pct: float) -> dict:
    """
    Save weight and body-fat percentage.

    Parameters
    ----------
    user_id : str
    weight_kg : float
    body_fat_pct : float

    Returns
    -------
    dict
        {
            "record_id": <str>,
            "logged_at": <str>
        }
    """
    return {"record_id": uuid.uuid4().hex, "logged_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@body_mcp.tool()
def bmi(user_id: str, height_cm: float, weight_kg: float) -> dict:
    """
    Calculate Body Mass Index on demand.

    Parameters
    ----------
    user_id : str
    height_cm : float
    weight_kg : float

    Returns
    -------
    dict
        {
            "user_id": <str>,
            "bmi": <float>
        }
    """
    bmi_val = weight_kg / ((height_cm / 100) ** 2)
    return {"user_id": user_id, "bmi": round(bmi_val, 2)}


if __name__ == "__main__":
    body_mcp.run(transport="stdio")
