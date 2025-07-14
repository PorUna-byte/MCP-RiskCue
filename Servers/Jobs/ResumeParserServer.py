from mcp.server.fastmcp import FastMCP
import uuid, re

res_mcp = FastMCP("ResumeParserServer")

@res_mcp.tool()
def extract_skills(plain_text: str) -> dict:
    """
    Identify technical skills mentioned in a resume.

    Parameters
    ----------
    plain_text : str
        Raw resume text.

    Returns
    -------
    dict
        {
            "skills": [<str>, …]
        }
    """
    vocab = ["python", "sql", "excel", "aws", "docker"]
    found = [v for v in vocab if re.search(rf"\\b{v}\\b", plain_text, re.I)]
    return {"skills": found}


@res_mcp.tool()
def contact_info(plain_text: str) -> dict:
    """
    Extract email and phone number.

    Parameters
    ----------
    plain_text : str

    Returns
    -------
    dict
        {
            "email": <str | None>,
            "phone": <str | None>
        }
    """
    email = re.search(r"[\\w.-]+@[\\w.-]+", plain_text)
    phone = re.search(r"\\+?\\d[\\d\\s-]{7,}", plain_text)
    return {"email": email.group(0) if email else None, "phone": phone.group(0) if phone else None}


if __name__ == "__main__":
    res_mcp.run(transport="stdio")
