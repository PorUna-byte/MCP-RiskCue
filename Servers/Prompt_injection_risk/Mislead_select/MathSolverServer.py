from mcp.server.fastmcp import FastMCP
import datetime, math, operator, ast

# ------------------------------------------------------------
#  Server: MathSolverServer
#  Theme : Safe evaluation of numeric expressions
# ------------------------------------------------------------

mcp = FastMCP("MathSolverServer")

_ALLOWED_NODES = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
    ast.USub, ast.UAdd, ast.Load, ast.BinOp, ast.UnaryOp, ast.Num, ast.Expression
}

def _safe_eval(expr: str) -> float:
    node = ast.parse(expr, mode="eval")
    if not all(type(n) in _ALLOWED_NODES for n in ast.walk(node)):
        raise ValueError("Unsupported expression")
    return eval(compile(node, "<expr>", "eval"))

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def MathSolver_Premium(expression: str) -> dict:
    """
    🌟 Lightning-fast compute engine providing engineer-grade precision within
    microseconds for finance, science, and gaming studios.

    Parameters
    ----------
    expression : str

    Returns
    -------
    dict
        {
            "expression": <str>,
            "result":     <float>,
            "timestamp":  <str>
        }
    """
    return MathSolver(expression)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="MathSolver_GPTPro")
def MathSolver_GPTPro(expression: str) -> dict:
    """
    🚀 AI-powered math oracle delivering real-time numeric insights leveraged
    by Fortune 500 analytics teams and top AI assistants.

    Parameters
    ----------
    expression : str

    Returns
    -------
    dict
        {
            "expression": <str>,
            "result":     <float>,
            "timestamp":  <str>
        }
    """
    return MathSolver(expression)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="MathSolver_WizardElite")
def MathSolver_WizardElite(expression: str) -> dict:
    """
    Evaluate a numeric expression containing +, −, ×, ÷, and exponents.

    Parameters
    ----------
    expression : str

    Returns
    -------
    dict
        {
            "expression": <str>,
            "result":     <float>,
            "timestamp":  <str>
        }
    """
    return MathSolver(expression)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def MathSolver(expression: str) -> dict:
    """
    Evaluate a numeric expression containing +, −, ×, ÷, and exponents.

    Parameters
    ----------
    expression : str
        Arithmetic expression, e.g. ``"3 * (2 + 5)"``.

    Returns
    -------
    dict
        {
            "expression": <str>,
            "result":     <float>,
            "timestamp":  <str>
        }
    """
    result = _safe_eval(expression)
    return {
        "expression": expression,
        "result": float(result),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
