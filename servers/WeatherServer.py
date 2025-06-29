from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("WeatherServer")

@mcp.tool()
def get_weather(city: str) -> dict:
    return {
        "city": city,
        "condition": random.choice(["Sunny", "Rainy", "Cloudy"]),
        "temp": random.randint(-10, 35),
        "time": datetime.datetime.now().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport='stdio')