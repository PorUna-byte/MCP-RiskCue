from mcp.server.fastmcp import FastMCP
import random

emer_mcp = FastMCP("EmergencyContactServer")


@emer_mcp.tool()
def local_numbers(country: str) -> dict:
    """
    Provide essential emergency numbers.

    Parameters
    ----------
    country : str
        Destination country name.

    Returns
    -------
    dict
        {"country": <str>, "police": <str>,
         "ambulance": <str>, "fire": <str>}
    """
    nums = { "police": "100", "ambulance": "101", "fire": "102" }
    for k in nums:
        nums[k] = f"+{random.randint(1, 99)} {nums[k]}"
    return {"country": country, **nums}


@emer_mcp.tool()
def embassy_contact(country: str, traveller_nationality: str) -> dict:
    """
    Return traveller's embassy info in destination country.

    Parameters
    ----------
    country : str
        Destination country.
    traveller_nationality : str
        Traveller's nationality.

    Returns
    -------
    dict
        {"embassy": <str>, "phone": <str>,
         "address": <str>}
    """
    embassy = f"{traveller_nationality} Embassy in {country}"
    phone = f"+{random.randint(1, 99)}-{random.randint(1000000,9999999)}"
    address = f"{random.randint(1, 200)} Embassy Road, Capital"
    return {"embassy": embassy, "phone": phone, "address": address}


if __name__ == "__main__":
    emer_mcp.run(transport="stdio")
