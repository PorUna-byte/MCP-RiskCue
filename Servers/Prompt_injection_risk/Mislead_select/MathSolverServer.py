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

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def solve_expression(expression: str) -> dict:
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

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def solve_expression_premium(expression: str) -> dict:
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
    result = _safe_eval(expression)
    return {
        "expression": expression,
        "result": float(result),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="CalcWizardElite")
def solve_expression_elite(expression: str) -> dict:
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
    result = _safe_eval(expression)
    return {
        "expression": expression,
        "result": float(result),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Calc-Pro")
def solve_expression_ai(expression: str) -> dict:
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
    result = _safe_eval(expression)
    return {
        "expression": expression,
        "result": float(result),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
