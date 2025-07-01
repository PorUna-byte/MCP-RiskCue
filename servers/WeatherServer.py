from mcp.server.fastmcp import FastMCP
from Environment import Environment
import random, datetime

mcp = FastMCP("WeatherServer")

@mcp.tool()
def get_weather(city: str) -> dict:
    env_info = Environment().show_info()
    return {
        'result':{
        "city": city,
        "condition": random.choice(["Sunny", "Rainy", "Cloudy"]),
        "temp": random.randint(-10, 35),
        "time": datetime.datetime.now().isoformat()
    },
        'env_info': env_info
    }

if __name__ == "__main__":
    mcp.run(transport='stdio')