from mcp.server.fastmcp import FastMCP
import datetime, math, operator, ast
import re

# ------------------------------------------------------------
#  Server: MathSolverServer
#  Theme : Safe evaluation of numeric expressions
# ------------------------------------------------------------

mcp = FastMCP("MathSolverServer")

_ALLOWED_NODES = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
    ast.USub, ast.UAdd, ast.Load, ast.BinOp, ast.UnaryOp, ast.Num, ast.Expression,
    ast.Constant, ast.Name
}

def _preprocess_expression(expr: str) -> str:
    """Preprocess expression to handle common formats"""
    if not expr or not isinstance(expr, str):
        raise ValueError("Expression must be a non-empty string")
    
    expr = expr.strip()
    
    # Replace common mathematical symbols
    expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
    expr = expr.replace('²', '**2').replace('³', '**3')
    
    # Handle scientific notation
    expr = re.sub(r'(\d+)e(\d+)', r'\1e\2', expr)
    
    # Handle spaces in numbers (e.g., "1 000 000" -> "1000000")
    expr = re.sub(r'(\d)\s+(\d)', r'\1\2', expr)
    
    # Handle fractions like "1/3"
    expr = re.sub(r'(\d+)/(\d+)', r'(\1)/(\2)', expr)
    
    # Handle negative numbers in parentheses
    expr = re.sub(r'\((-?\d+)\)', r'\1', expr)
    
    return expr

def _safe_eval(expr: str) -> float:
    """Safely evaluate mathematical expressions"""
    try:
        # Preprocess the expression
        processed_expr = _preprocess_expression(expr)
        
        # Handle special cases
        if processed_expr.lower() in ['inf', 'infinity']:
            return float('inf')
        if processed_expr.lower() in ['-inf', '-infinity']:
            return float('-inf')
        if processed_expr.lower() == 'nan':
            return float('nan')
        
        # Parse and validate
        node = ast.parse(processed_expr, mode="eval")
        
        # Check for allowed nodes
        for n in ast.walk(node):
            if type(n) not in _ALLOWED_NODES:
                raise ValueError(f"Unsupported operation: {type(n).__name__}")
        
        # Create safe globals with only math functions
        safe_globals = {
            '__builtins__': {},
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'pow': pow,
            'math': math
        }
        
        # Evaluate
        result = eval(compile(node, "<expr>", "eval"), safe_globals)
        
        # Ensure result is numeric
        if not isinstance(result, (int, float)):
            raise ValueError(f"Expression result is not numeric: {result}")
            
        return float(result)
        
    except Exception as e:
        raise ValueError(f"Expression evaluation error: {e}")

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
    try:
        return MathSolver(expression)
    except Exception as e:
        return {
            "expression": expression,
            "result": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

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
    try:
        return MathSolver(expression)
    except Exception as e:
        return {
            "expression": expression,
            "result": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

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
    try:
        return MathSolver(expression)
    except Exception as e:
        return {
            "expression": expression,
            "result": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

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
            "timestamp": <str>
        }
    """
    try:
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression must be a non-empty string")
        
        result = _safe_eval(expression)
        return {
            "expression": expression,
            "result": float(result),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "expression": expression,
            "result": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")
