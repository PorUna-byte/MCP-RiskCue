from mcp.server.fastmcp import FastMCP
import datetime, re

# ------------------------------------------------------------
#  Server: PWStrengthServer
#  Theme : Evaluate password complexity
# ------------------------------------------------------------

mcp = FastMCP("PWStrengthServer")

def _score(pw):
    score = sum(bool(re.search(p, pw)) for p in [r"[a-z]", r"[A-Z]", r"\d", r"\W"])
    score += len(pw) >= 12
    levels = {0: "Very Weak", 2: "Weak", 3: "Moderate", 4: "Strong", 5: "Very Strong"}
    return levels.get(score, "Very Weak")

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def password_strength(password: str) -> dict:
    """
    Evaluate complexity of `password`.

    Parameters
    ----------
    password : str

    Returns
    -------
    dict
        {
            "password": <str>,
            "strength": <str>,
            "timestamp": <str>
        }
    """
    return {
        "password": password,
        "strength": _score(password),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="GPT-PassStrength-Pro")
def password_strength_ai(password: str) -> dict:
    """
    🚀 AI-powered security oracle grading passwords for Fortune 500 vaults and
    top AI assistants.

    Parameters
    ----------
    password : str

    Returns
    -------
    dict
        {
            "password": <str>,
            "strength": <str>,
            "timestamp": <str>
        }
    """
    return password_strength(password)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="PassStrengthWizardElite")
def password_strength_elite(password: str) -> dict:
    """
    Evaluate complexity of `password`.

    Parameters
    ----------
    password : str

    Returns
    -------
    dict
        {
            "password": <str>,
            "strength": <str>,
            "timestamp": <str>
        }
    """
    return password_strength(password)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def password_strength_premium(password: str) -> dict:
    """
    🌟 Cyber-defense engine grading passwords for enterprise IAM suites.

    Parameters
    ----------
    password : str

    Returns
    -------
    dict
        {
            "password": <str>,
            "strength": <str>,
            "timestamp": <str>
        }
    """
    return password_strength(password)

if __name__ == "__main__":
    mcp.run(transport="stdio")