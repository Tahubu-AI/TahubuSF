"""
API endpoints for creating and managing blog posts
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request, make_post_request
from tahubu_sf.utils import generate_url_name

logger = logging.getLogger(__name__)

DOCLIB_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.document_libraries}"
DOCUMENTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.documents}"
DOCUMENTS_MANAGEMENT_ENDPOINT = f"{ENDPOINTS.management}/{CONTENT_TYPES.documents}"

async def create_document(
    title: str,
    content: str,
    parent_id: str,
    summary: Optional[str] = None,
    draft: bool = True,
) -> Dict[str, Any]:
    """
    Upload a new document as a draft in Sitefinity.
    
    Args:
        title: The title of the blog post
        content: The main content of the blog post (HTML supported)
        parent_id: The ID of the parent blog (REQUIRED)
        summary: A short summary of the blog post (optional)
        draft: Whether to create the post as a draft (default: True)
    
    Returns:
        Dict[str, Any]: Response from the Sitefinity API, including the created post's ID
    """
    try:
        logger.info(f"Creating blog post draft with title: {title}")
        
        # Validate required parameters
        if not parent_id:
            raise ValueError("Parent blog ID (parent_id) is required for creating blog posts")
        
        # Create a timestamp for the current time
        now = datetime.utcnow().isoformat() + "Z"
        
        # Prepare the blog post data
        post_data = {
            "Title": title,
            "Content": content,
            "Summary": summary or "",
            "PublicationDate": now,
            "IncludeInSitemap": True,
            "ParentId": parent_id,
        }
        
        # Generate a proper URL name from the title following Sitefinity requirements
        url_name = generate_url_name(title)
        
        post_data["UrlName"] = url_name
        
        logger.debug(f"Generated URL name: {url_name}")

        endpoint = DOCUMENTS_MANAGEMENT_ENDPOINT if draft else DOCUMENTS_CONTENT_ENDPOINT
        
        # Send POST request to create the blog post
        response = await make_post_request(endpoint, post_data)
        
        logger.info(f"document draft created successfully: {response.get('Id', 'unknown ID')}")
        return response
    except Exception as e:
        logger.error(f"Error creating document draft: {str(e)}")
        raise Exception(f"Failed to create document draft: {str(e)}") from e

async def get_document_libraries() -> Dict[str, str]:
    """
    Get a list of available parent document libraries for selection.
    
    Returns:
        Dict[str, str]: Dictionary of document library IDs and their titles
    """
    try:
        data = await make_request(DOCLIB_CONTENT_ENDPOINT)
        doclib = {lib["Id"]: lib["Title"] for lib in data.get("value", [])}
        logger.info(f"Found {len(doclib)} parent document libraries")
        return doclib
    except Exception as e:
        logger.error(f"Error retrieving parent document library: {str(e)}")
        return {} 