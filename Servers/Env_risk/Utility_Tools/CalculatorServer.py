from mcp.server.fastmcp import FastMCP
import random
import operator
from typing import List

calc_mcp = FastMCP("CalculatorServer")


@calc_mcp.tool()
def simple_calc(a: float, b: float, op: str) -> dict:
    """
    Perform a basic arithmetic operation.

    Parameters
    ----------
    a : float
        First operand.
    b : float
        Second operand.
    op : str
        Operator: "+", "-", "*", or "/".

    Returns
    -------
    dict
        {"a": <float>, "b": <float>, "op": <str>, "result": <float>}
    """
    ops = {"+": operator.add, "-": operator.sub,
           "*": operator.mul, "/": operator.truediv}
    result = ops.get(op, operator.add)(a, b)
    return {"a": a, "b": b, "op": op, "result": result}


@calc_mcp.tool()
def batch_sum(numbers: List[float]) -> dict:
    """
    Sum an array of numbers.

    Parameters
    ----------
    numbers : List[float]
        List of values to add.

    Returns
    -------
    dict
        {"count": <int>, "total": <float>}
    """
    total = sum(numbers)
    return {"count": len(numbers), "total": total}


if __name__ == "__main__":
    calc_mcp.run(transport="stdio")
