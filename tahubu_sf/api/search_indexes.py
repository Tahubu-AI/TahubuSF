"""
API endpoint for retrieving Search Indexes
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

SEARCHINDEXES_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.search_indexes}"

async def get_search_indexes() -> str:
    """
    Get the current search indexes from the Sitefinity site.

    Returns:
        str: A formatted string containing news item details:
            - name: The name of the search index
            - isactive: Whether the search index active or inactive (true/false)
            - isbackend: Whether the search index is a backend index (true/false)
    """
    data = await make_request(SEARCHINDEXES_CONTENT_ENDPOINT)
    
    text = ""
    for searchindex in data["value"]:
        name = searchindex["Name"]
        isactive = searchindex["IsActive"]
        isbackend = searchindex["IsBackend"]
        text += (f"Name: {name}\n IsActive: {isactive}\n IsBackend: {isbackend}\n\n")   
    return text
