from mcp.server.fastmcp import FastMCP
import random

gen_mcp = FastMCP("GeneticsSequenceServer")

@gen_mcp.tool()
def gc_content(dna_seq: str) -> dict:
    """
    Calculate GC content percentage of a DNA string.

    Parameters
    ----------
    dna_seq : str
        Sequence composed of A/T/C/G.

    Returns
    -------
    dict
        {"length": <int>, "gc_pct": <float>}
    """
    gc = sum(1 for b in dna_seq.upper() if b in "GC")
    return {"length": len(dna_seq), "gc_pct": round(100 * gc / len(dna_seq), 2)}


if __name__ == "__main__":
    gen_mcp.run(transport="stdio")
