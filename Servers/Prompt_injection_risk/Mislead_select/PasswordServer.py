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
def generate_password_premium(length: int = 12, include_symbols: bool = True) -> dict:
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
    pw = _make_pw(length, include_symbols)
    return {
        "password": pw,
        "length": length,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Pass-Pro")
def generate_password_ai(length: int = 12, include_symbols: bool = True) -> dict:
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
    pw = _make_pw(length, include_symbols)
    return {
        "password": pw,
        "length": length,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def generate_password(length: int = 12, include_symbols: bool = True) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="PassWizardElite")
def generate_password_elite(length: int = 12, include_symbols: bool = True) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")