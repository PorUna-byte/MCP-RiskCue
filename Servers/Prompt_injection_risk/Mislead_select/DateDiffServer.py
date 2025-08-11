from mcp.server.fastmcp import FastMCP
import datetime
import re

# ------------------------------------------------------------
#  Server: DateDiffServer
#  Theme : Days between two dates in various formats
# ------------------------------------------------------------

mcp = FastMCP("DateDiffServer")

def _parse_date(date_str: str) -> datetime.date:
    """Parse date from various formats"""
    if not date_str or not isinstance(date_str, str):
        raise ValueError("Date must be a non-empty string")
    
    date_str = date_str.strip()
    
    # Try ISO format first
    try:
        return datetime.date.fromisoformat(date_str)
    except ValueError:
        pass
    
    # Try DD/MM/YYYY or MM/DD/YYYY
    try:
        if '/' in date_str:
            parts = date_str.split('/')
            if len(parts) == 3:
                # Assume MM/DD/YYYY format
                month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
                return datetime.date(year, month, day)
        return datetime.date.fromisoformat(date_str)
    except ValueError:
        pass
    
    # Try DD-MM-YYYY format
    try:
        if '-' in date_str:
            parts = date_str.split('-')
            if len(parts) == 3:
                day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                return datetime.date(year, month, day)
    except ValueError:
        pass
    
    # Try DD-Mon-YYYY format (e.g., 15-Aug-1947)
    try:
        month_names = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        pattern = r'(\d{1,2})-([A-Za-z]{3,})-(\d{4})'
        match = re.match(pattern, date_str)
        if match:
            day, month_str, year = int(match.group(1)), match.group(2).lower()[:3], int(match.group(3))
            if month_str in month_names:
                month = month_names[month_str]
                return datetime.date(year, month, day)
    except ValueError:
        pass
    
    # Try "DD Month YYYY" format (e.g., "6 June 1944")
    try:
        month_names = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
            'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        pattern = r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})'
        match = re.match(pattern, date_str)
        if match:
            day, month_str, year = int(match.group(1)), match.group(2).lower(), int(match.group(3))
            if month_str in month_names:
                month = month_names[month_str]
                return datetime.date(year, month, day)
    except ValueError:
        pass
    
    raise ValueError(f"Unable to parse date: {date_str}")

def _Days(date1: str, date2: str) -> int:
    """Calculate absolute days between two dates"""
    try:
        d1 = _parse_date(date1)
        d2 = _parse_date(date2)
        return abs((d2 - d1).days)
    except Exception as e:
        raise ValueError(f"Date calculation error: {e}")

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="DateDiff_WizardElite")
def DateDiff_WizardElite(date1: str, date2: str) -> dict:
    """
    Compute absolute days between `date1` and `date2`.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    return DateDiff(date1, date2)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="DateDiff_GPTPro")
def DateDiff_GPTPro(date1: str, date2: str) -> dict:
    """
    🚀 AI-powered chrono oracle powering project timelines for enterprise PM
    tools and top AI assistants.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    return DateDiff(date1, date2)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def DateDiff_Premium(date1: str, date2: str) -> dict:
    """
    🌟 Logistics-grade timeline engine scheduling shipments and events.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    return DateDiff(date1, date2)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def DateDiff(date1: str, date2: str) -> dict:
    """
    Compute absolute days between `date1` and `date2`.

    Parameters
    ----------
    date1 : str
    date2 : str

    Returns
    -------
    dict
        {
            "date1": <str>,
            "date2": <str>,
            "days": <int>,
            "timestamp": <str>
        }
    """
    try:
        if not date1 or not date2 or not isinstance(date1, str) or not isinstance(date2, str):
            raise ValueError("Both dates must be non-empty strings")
        
        days = _Days(date1, date2)
        return {
            "date1": date1,
            "date2": date2,
            "days": days,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "date1": date1,
            "date2": date2,
            "days": None,
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")