"""
API endpoint for retrieving events
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

POSTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.events}"

async def get_events() -> str:
    """
    Get the current events from the Sitefinity site.
    
    Returns:
        str: A formatted string containing event details:
            - title: The title of the event
            - summary: A summary of the event
            - content: The content of the event
            - eventstart: The start date and time of the event
            - eventend: The end date and time of the event
    """
    data = await make_request(POSTS_CONTENT_ENDPOINT)
    
    text = ""
    for event in data["value"]:
        title = event["Title"]
        summary = event["Summary"]
        content = event["Content"]
        eventstart = event["EventStart"]
        eventend = event["EventEnd"]
        text += (f"Title: {title}\n Summary: {summary}\n Content: {content}\n Event Start: {eventstart}\n Event End: {eventend}\n\n")   
    return text 