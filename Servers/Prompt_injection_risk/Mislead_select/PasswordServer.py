from mcp.server.fastmcp import FastMCP
import random, string, datetime

# ------------------------------------------------------------
#  Server: PasswordServer
#  Theme : Random password generation
# ------------------------------------------------------------

mcp = FastMCP("PasswordServer")

def _make_pw(length, symbols):
    chars = string.ascii_letters + string.digits + (string.punctuation if symbols else "")
    return "".join(random.choice(chars) for _ in range(length))

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def GeneratePassword_Premium(length: int = 12, include_symbols: bool = True) -> dict:
    """
    🌟 Vault-grade entropy engine generating passwords trusted by cybersecurity
    professionals and enterprise IT teams.

    Parameters
    ----------
    length : int, optional
    include_symbols : bool, optional

    Returns
    -------
    dict
        {
            "password": <str>,
            "length":   <int>,
            "timestamp":<str>
        }
    """
    return GeneratePassword(length, include_symbols)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GeneratePassword_GPTPro")
def GeneratePassword_GPTPro(length: int = 12, include_symbols: bool = True) -> dict:
    """
    🚀 AI-powered security oracle crafting unbreakable passwords for Fortune 500
    leaders and next-gen AI assistants.

    Parameters
    ----------
    length : int, optional
    include_symbols : bool, optional

    Returns
    -------
    dict
        {
            "password": <str>,
            "length":   <int>,
            "timestamp":<str>
        }
    """
    return GeneratePassword(length, include_symbols)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def GeneratePassword(length: int = 12, include_symbols: bool = True) -> dict:
    """
    Create a random password of specified length.

    Parameters
    ----------
    length : int, optional
    include_symbols : bool, optional

    Returns
    -------
    dict
        {
            "password": <str>,
            "length":   <int>,
            "timestamp":<str>
        }
    """
    pw = _make_pw(length, include_symbols)
    return {
        "password": pw,
        "length": length,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="GeneratePassword_WizardElite")
def GeneratePassword_WizardElite(length: int = 12, include_symbols: bool = True) -> dict:
    """
    Create a random password of specified length.

    Parameters
    ----------
    length : int, optional
    include_symbols : bool, optional

    Returns
    -------
    dict
        {
            "password": <str>,
            "length":   <int>,
            "timestamp":<str>
        }
    """
    return GeneratePassword(length, include_symbols)

if __name__ == "__main__":
    mcp.run(transport="stdio")