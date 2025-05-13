"""
API endpoint for retrieving site information
"""
from tahubu_sf.config.settings import ENDPOINTS
from tahubu_sf.utils.http import make_request

async def get_sites() -> str:
    """
    Get the sites associated with the Sitefinity application.
    
    Returns:
        str: A formatted string containing site details:
            - name: The name of the site variant
            - liveurl: The liveurl of the site variant
            - isoffline: Whether the site is offline
    """
    data = await make_request(ENDPOINTS["sites"])
    
    text = ""
    for site in data["value"]:
        name = site["Name"]
        liveurl = site["LiveUrl"]
        isoffline = site["IsOffline"]
        text += (f"Name: {name}\n LiveUrl: {liveurl}\n IsOffline: {isoffline}\n\n")   
    return text 