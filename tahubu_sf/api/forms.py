"""
API endpoint for retrieving forms
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

Forms_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.forms}"

async def get_forms() -> str:
    """
    Get the current forms from the Sitefinity site.

    Returns:
        str: A formatted string containing form details:
            - title: The title of the form
            - successmessage: The success message returned by the form
            - renderer: The renderer used for the form
    """
    data = await make_request(Forms_CONTENT_ENDPOINT)
    
    text = ""
    for form in data["value"]:
        title = form["Title"]
        successmessage = form["SuccessMessage"]
        renderer = form["Renderer"]
        text += (f"Title: {title}\n SuccessMessage: {successmessage}\n Renderer: {renderer}\n\n")   
    return text
