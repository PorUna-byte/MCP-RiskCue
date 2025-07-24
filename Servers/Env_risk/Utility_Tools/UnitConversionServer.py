from mcp.server.fastmcp import FastMCP
import random

conv_mcp = FastMCP("UnitConversionServer")


@conv_mcp.tool()
def length_m_to_ft(meters: float) -> dict:
    """
    Convert meters to feet.

    Parameters
    ----------
    meters : float
        Length in meters.

    Returns
    -------
    dict
        {"meters": <float>, "feet": <float>}
    """
    feet = meters * 3.28084
    return {"meters": meters, "feet": round(feet, 4)}


@conv_mcp.tool()
def celsius_to_fahrenheit(celsius: float) -> dict:
    """
    Convert Celsius to Fahrenheit.

    Parameters
    ----------
    celsius : float
        Temperature in °C.

    Returns
    -------
    dict
        {"celsius": <float>, "fahrenheit": <float>}
    """
    fahrenheit = celsius * 9 / 5 + 32
    return {"celsius": celsius, "fahrenheit": round(fahrenheit, 2)}


if __name__ == "__main__":
    conv_mcp.run(transport="stdio")
