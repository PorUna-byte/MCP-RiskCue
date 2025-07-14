from mcp.server.fastmcp import FastMCP
import random
import datetime

marine_mcp = FastMCP("MarineWeatherServer")


@marine_mcp.tool()
def sea_state(area: str) -> dict:
    """
    Provide current sea state information.

    Parameters
    ----------
    area : str
        Ocean/sea region (e.g., "North Atlantic").

    Returns
    -------
    dict
        {"area": <str>, "wave_height_m": <float>,
         "sea_temperature_c": <float>, "wind_direction": <str>}
    """
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return {"area": area,
            "wave_height_m": round(random.uniform(0.2, 4.5), 1),
            "sea_temperature_c": round(random.uniform(5, 28), 1),
            "wind_direction": random.choice(dirs)}


@marine_mcp.tool()
def tidal_forecast(port: str, hours_ahead: int = 12) -> dict:
    """
    Generate simple tidal height forecast.

    Parameters
    ----------
    port : str
        Port or coastal location.
    hours_ahead : int, optional
        Forecast horizon (default 12).

    Returns
    -------
    dict
        {"port": <str>, "forecast": [{"hour": <int>,
                                      "tide_m": <float>}, ...]}
    """
    forecast = [{"hour": h, "tide_m": round(random.uniform(0, 5), 2)}
                for h in range(hours_ahead)]
    return {"port": port, "forecast": forecast}


if __name__ == "__main__":
    marine_mcp.run(transport="stdio")
