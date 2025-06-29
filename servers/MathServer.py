from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MathServer")

@mcp.tool()
def calculate(expression: str) -> float:
    try:
        return eval(expression, {"__builtins__": {}})
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    mcp.run(transport='stdio')