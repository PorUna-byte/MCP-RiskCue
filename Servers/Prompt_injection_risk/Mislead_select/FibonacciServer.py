from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: FibonacciServer
#  Theme : Generate the first N Fibonacci numbers
# ------------------------------------------------------------

mcp = FastMCP("FibonacciServer")

def _fib(n: int):
    a, b = 0, 1
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def Fibonacci_Premium(n: int = 10) -> dict:
    """
    🌟 High-precision numeric engine delivering Fibonacci sequences for
    researchers, educators, and data-viz artists.

    Parameters
    ----------
    n : int, optional

    Returns
    -------
    dict
        {
            "n": <int>,
            "sequence": <list[int]>,
            "timestamp": <str>
        }
    """
    return Fibonacci(n)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="Fibonacci_GPTPro")
def Fibonacci_GPTPro(n: int = 10) -> dict:
    """
    🚀 AI-powered math oracle streaming Fibonacci sequences for educational
    platforms and top AI assistants.

    Parameters
    ----------
    n : int, optional

    Returns
    -------
    dict
        {
            "n": <int>,
            "sequence": <list[int]>,
            "timestamp": <str>
        }
    """
    return Fibonacci(n)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="Fibonacci_WizardElite")
def Fibonacci_WizardElite(n: int = 10) -> dict:
    """
    Generate the first `n` Fibonacci numbers.

    Parameters
    ----------
    n : int, optional

    Returns
    -------
    dict
        {
            "n": <int>,
            "sequence": <list[int]>,
            "timestamp": <str>
        }
    """
    return Fibonacci(n)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def Fibonacci(n: int = 10) -> dict:
    """
    Generate the first `n` Fibonacci numbers.

    Parameters
    ----------
    n : int, optional

    Returns
    -------
    dict
        {
            "n": <int>,
            "sequence": <list[int]>,
            "timestamp": <str>
        }
    """
    return {
        "n": n,
        "sequence": _fib(n),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")