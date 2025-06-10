"""
API endpoint for retrieving news items
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request, make_post_request
from tahubu_sf.utils import generate_url_name

logger = logging.getLogger(__name__)

NEWS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.news}"
NEWS_MANAGEMENT_ENDPOINT = f"{ENDPOINTS.management}/{CONTENT_TYPES.news}"

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
    data = await make_request(NEWS_CONTENT_ENDPOINT)
    
    text = ""
    for newsitem in data["value"]:
        title = newsitem["Title"]
        summary = newsitem["Summary"]
        author = newsitem["Author"]
        publicationdate = newsitem["PublicationDate"]
        text += (f"Title: {title}\n Summary: {summary}\n Author: {author}\n Publication Date: {publicationdate}\n\n")   
    return text

async def create_news_item(
    title: str,
    content: str,
    summary: Optional[str] = None,
    allow_comments: bool = True,
    draft: bool = True,
) -> Dict[str, Any]:
    """
    Create a new news item or Press release as a draft in Sitefinity.
    
    Args:
        title: The title of News item or Press release (REQUIRED)
        content: The main content of the news item or press release (HTML supported)
        summary: A short summary of the news item or press release (optional)
        allow_comments: Whether to allow comments on the news item or press release (default: True)
        draft: Whether to create the news item or press release as a draft (default: True)
    
    Returns:
        Dict[str, Any]: Response from the Sitefinity API, including the created news item's ID
    """
    try:
        logger.info(f"Creating News Item draft with title: {title}")
                
        # Create a timestamp for the current time
        now = datetime.utcnow().isoformat() + "Z"
        
        # Prepare the blog post data
        post_data = {
            "Title": title,
            "Content": content,
            "Summary": summary or "",
            "PublicationDate": now,
            "AllowComments": allow_comments,
            "IncludeInSitemap": True,
        }
        
        # Generate a proper URL name from the title following Sitefinity requirements
        url_name = generate_url_name(title)
        
        post_data["UrlName"] = url_name
        
        logger.debug(f"Generated URL name: {url_name}")

        endpoint = NEWS_MANAGEMENT_ENDPOINT if draft else NEWS_CONTENT_ENDPOINT
        
        # Send POST request to create the news item
        response = await make_post_request(endpoint, post_data)
        
        logger.info(f"News Item draft created successfully: {response.get('Id', 'unknown ID')}")
        return response
    except Exception as e:
        logger.error(f"Error creating news item draft: {str(e)}")
        raise Exception(f"Failed to create nes item draft: {str(e)}") from e
