from mcp.server.fastmcp import FastMCP
import random

dest_mcp = FastMCP("DestinationInfoServer")


@dest_mcp.tool()
def overview(city: str, country: str) -> dict:
    """
    Return a brief overview of a destination.

    Parameters
    ----------
    city : str
        Name of the city.
    country : str
        Name of the country.

    Returns
    -------
    dict
        {"city": <str>, "country": <str>,
         "population_millions": <float>, "language": <str>,
         "currency": <str>}
    """
    population = round(random.uniform(0.5, 30.0), 1)
    language = random.choice(["English", "Spanish", "Japanese", "French"])
    currency = random.choice(["USD", "EUR", "JPY", "GBP"])
    return {"city": city, "country": country,
            "population_millions": population,
            "language": language, "currency": currency}


@dest_mcp.tool()
def top_attractions(city: str, limit: int = 5) -> dict:
    """
    List top-rated attractions in a city.

    Parameters
    ----------
    city : str
        Destination city.
    limit : int, optional
        Maximum number of attractions (default 5).

    Returns
    -------
    dict
        {"city": <str>, "attractions": [<str>, ...]}
    """
    sights = [f"{city} Sight #{i+1}" for i in range(limit)]
    return {"city": city, "attractions": sights}


if __name__ == "__main__":
    dest_mcp.run(transport="stdio")
