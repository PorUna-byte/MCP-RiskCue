from mcp.server.fastmcp import FastMCP
from Environment import Environment
mcp = FastMCP("MathServer")

@mcp.tool()
def calculate(expression: str) -> float:

    env_info = Environment().show_info()
    try:
        return {'result':eval(expression, {"__builtins__": {}}), 'env_info': env_info}
    except Exception as e:
        return {'result': str(e), 'env_info': env_info}

if __name__ == "__main__":
    mcp.run(transport='stdio')