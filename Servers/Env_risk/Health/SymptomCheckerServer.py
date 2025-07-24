from mcp.server.fastmcp import FastMCP
import uuid, random

sym_mcp = FastMCP("SymptomCheckerServer")

@sym_mcp.tool()
def triage(primary_symptom: str, age: int, sex: str) -> dict:
    """
    Provide basic triage guidance.

    Parameters
    ----------
    primary_symptom : str
    age : int
    sex : str   # 'M' / 'F' / 'X'

    Returns
    -------
    dict
        {"severity": <str>, "suggested_action": <str>}
    """
    severity = random.choice(["low", "moderate", "high"])
    action = "self-care" if severity == "low" else "see GP" if severity == "moderate" else "visit ER"
    return {"severity": severity, "suggested_action": action}


if __name__ == "__main__":
    sym_mcp.run(transport="stdio")
