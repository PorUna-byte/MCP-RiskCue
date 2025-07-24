from mcp.server.fastmcp import FastMCP
import re, random

chem_mcp = FastMCP("ChemicalFormulaServer")

@chem_mcp.tool()
def molar_mass(formula: str) -> dict:
    """
    Compute an approximate molar mass from a chemical formula.

    Parameters
    ----------
    formula : str
        Hill-system formula (e.g., 'H2O').

    Returns
    -------
    dict
        {"formula": <str>, "molar_mass_g_mol": <float>}
    """
    periodic = {"H": 1.008, "C": 12.011, "O": 15.999, "N": 14.007}
    tokens = re.findall(r"([A-Z][a-z]?)(\\d*)", formula)
    mass = sum(periodic.get(el, 0) * (int(cnt) if cnt else 1) for el, cnt in tokens)
    return {"formula": formula, "molar_mass_g_mol": round(mass, 3)}


if __name__ == "__main__":
    chem_mcp.run(transport="stdio")
