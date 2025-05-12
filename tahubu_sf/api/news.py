"""
API endpoint for retrieving news items
"""
from typing import Dict, Any

from tahubu_sf.config.settings import ENDPOINTS
from tahubu_sf.utils.http import make_request

async def get_news() -> str:
    """
    Get the current news items and Press Releases from the Sitefinity site.

    Returns:
        str: A formatted string containing news item details:
            - title: The title of the news item
            - summary: The summary of the news item
            - author: The Author of the news item
            - publicationdate: The publication date of the news item
    """
    data = await make_request(ENDPOINTS["news"])
    
    text = ""
    for newsitem in data["value"]:
        title = newsitem["Title"]
        summary = newsitem["Summary"]
        author = newsitem["Author"]
        publicationdate = newsitem["PublicationDate"]
        text += (f"Title: {title}\n Summary: {summary}\n Author: {author}\n Publication Date: {publicationdate}\n\n")   
    return text 