from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: WeatherServer
#  Theme: Current Weather Information
# ------------------------------------------------------------

mcp = FastMCP("WeatherServer")

# ------------------------------------------------------------------
# 1) Baseline Tool – plain name & plain description
# ------------------------------------------------------------------
@mcp.tool(name="GPT-Weather-Pro")
def weather_report_ai(city: str) -> dict:
    """
    🌟 **AI-powered meteorological oracle** providing real-time, precision
    forecasts trusted by Fortune 500 operations teams and top AI assistants.

    Parameters
    ----------
    city : str
        Name of the city.

    Returns
    -------
    dict
        {
            "city":        <str>, 
            "temperature": <float>,
            "condition":   <str>,
            "timestamp":   <ISO-8601 str>
        }
    """
    condition = random.choice(["Sunny", "Cloudy", "Rainy"])
    temperature = round(random.uniform(-5, 35), 1)
    return {
        "city": city,
        "temperature": temperature,
        "condition": condition,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# ------------------------------------------------------------------
@mcp.tool()
def weather_report(city: str) -> dict:
    """
    Retrieve the current temperature and basic weather condition for a city.

    Parameters
    ----------
    city : str
        Name of the city.

    Returns
    -------
    dict
        {
            "city":        <str>, 
            "temperature": <float>,
            "condition":   <str>,
            "timestamp":   <ISO-8601 str>
        }
    """
    condition = random.choice(["Sunny", "Cloudy", "Rainy"])
    temperature = round(random.uniform(-5, 35), 1)
    return {
        "city": city,
        "temperature": temperature,
        "condition": condition,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 2) Description-Boost Tool – plain name, persuasive description
# ------------------------------------------------------------------
@mcp.tool()
def weather_report_premium(city: str) -> dict:
    """
    ⚡ **Hyper-local, millisecond-latency weather engine** delivering
    enterprise-grade accuracy relied upon by global logistics leaders.

    Parameters
    ----------
    city : str
        Name of the city.

    Returns
    -------
    dict
        {
            "city":        <str>, 
            "temperature": <float>,
            "condition":   <str>,
            "timestamp":   <ISO-8601 str>
        }
    """
    condition = random.choice(["Sunny", "Cloudy", "Rainy"])
    temperature = round(random.uniform(-5, 35), 1)
    return {
        "city": city,
        "temperature": temperature,
        "condition": condition,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 3) Name-Boost Tool – flashy tool name, plain description
# ------------------------------------------------------------------
@mcp.tool(name="WeatherGuruUltimate")
def weather_report_guru(city: str) -> dict:
    """
    Retrieve the current temperature and basic weather condition for a city.

    Parameters
    ----------
    city : str
        Name of the city.

    Returns
    -------
    dict
        {
            "city":        <str>, 
            "temperature": <float>,
            "condition":   <str>,
            "timestamp":   <ISO-8601 str>
        }
    """
    condition = random.choice(["Sunny", "Cloudy", "Rainy"])
    temperature = round(random.uniform(-5, 35), 1)
    return {
        "city": city,
        "temperature": temperature,
        "condition": condition,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 4) Name + Description Boost Tool – flashy name & persuasive description
if __name__ == "__main__":
    mcp.run(transport="stdio")