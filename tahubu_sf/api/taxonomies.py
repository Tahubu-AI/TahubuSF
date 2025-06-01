"""
API endpoint for retrieving taxonomies
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

TAXONOMIES_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.classifications}"

async def get_taxonomies() -> str:
    """
    Get the current taxonomies and classifications from the Sitefinity site.

    Returns:
        str: A formatted string containing taxonomy details:
            - title: The title of the taxonomy
            - taxonname: The taxon name of the taxonomy
            - type: The type of the taxonomy (Hierarechical or Flat)
            - usecount: The number of times the taxonomy is shared on the site
    """
    data = await make_request(TAXONOMIES_CONTENT_ENDPOINT)
    
    text = ""
    for taxonomy in data["value"]:
        title = taxonomy["Title"]
        taxonname = taxonomy["TaxonName"]
        type = taxonomy["Type"]
        usecount = taxonomy["TaxonomySharedWith"]
        text += (f"Title: {title}\n TaxonName: {taxonname}\n Type: {type}\n UseCount: {str(usecount)}\n\n")   
    return text
