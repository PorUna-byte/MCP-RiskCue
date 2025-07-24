from mcp.server.fastmcp import FastMCP

phys_mcp = FastMCP("PhysicsConstantServer")

@phys_mcp.tool()
def get_constant(symbol: str) -> dict:
    """
    Return the accepted SI value of a physical constant.

    Parameters
    ----------
    symbol : str
        Constant symbol (e.g., 'c', 'h', 'G').

    Returns
    -------
    dict
        {"symbol": <str>, "value": <float>, "unit": <str>}
    """
    constants = {
        "c": 299_792_458.0,            # m/s
        "h": 6.62607015e-34,           # J·s
        "G": 6.67430e-11,              # m³·kg⁻¹·s⁻²
        "k": 1.380649e-23,             # J·K⁻¹
    }
    units = {
        "c": "m s^-1",
        "h": "J s",
        "G": "m^3 kg^-1 s^-2",
        "k": "J K^-1",
    }
    return {"symbol": symbol, "value": constants.get(symbol), "unit": units.get(symbol)}


@phys_mcp.tool()
def list_constants() -> dict:
    """
    List available constant symbols.

    Returns
    -------
    dict
        {"symbols": [<str>, …]}
    """
    return {"symbols": ["c", "h", "G", "k"]}


if __name__ == "__main__":
    phys_mcp.run(transport="stdio")
