"""
API endpoints for creating and managing images
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request, make_post_request
from tahubu_sf.utils import generate_url_name

logger = logging.getLogger(__name__)

ALBUMS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.albums}"
IMAGES_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.images}"
IMAGES_MANAGEMENT_ENDPOINT = f"{ENDPOINTS.management}/{CONTENT_TYPES.images}"

async def create_image(
    title: str,
    dalle_prompt: str,
    parent_id: str,
    draft: bool = True,
) -> Dict[str, Any]:
    """
    Create a new image as a draft in Sitefinity.
    
    Args:
        title: The title of the list item (REQUIRED)
        dalle_prompt: The dalle prompt to create the image using DALL-E LLM
        parent_id: The ID of the parent list (REQUIRED)
        draft: Whether to create the list item as a draft (default: True)
    
    Returns:
        Dict[str, Any]: Response from the Sitefinity API, including the created image's ID
    """
    try:
        logger.info(f"Creating image draft with title: {title}")
        
        # Validate required parameters
        if not parent_id:
            raise ValueError("Parent image ID (parent_id) is required for creating images")
        
        # Create a timestamp for the current time
        now = datetime.utcnow().isoformat() + "Z"
        
        # Prepare the list item data
        post_data = {
            "Title": title,
            "Dalle_prompt": dalle_prompt,
            "PublicationDate": now,
            "ParentId": parent_id,
        }
        
        # Generate a proper URL name from the title following Sitefinity requirements
        url_name = generate_url_name(title)
        
        post_data["UrlName"] = url_name
        
        logger.debug(f"Generated URL name: {url_name}")

        endpoint = IMAGES_MANAGEMENT_ENDPOINT if draft else IMAGES_CONTENT_ENDPOINT
        
        # Send POST request to create the List Item
        response = await make_post_request(endpoint, post_data)
        
        logger.info(f"Image draft created successfully: {response.get('Id', 'unknown ID')}")
        return response
    except Exception as e:
        logger.error(f"Error creating Image draft: {str(e)}")
        raise Exception(f"Failed to create Image draft: {str(e)}") from e

async def get_albums() -> Dict[str, str]:
    """
    Get a list of available parent album for selection.
    
    Returns:
        Dict[str, str]: Dictionary of Album IDs and their titles
    """
    try:
        data = await make_request(ALBUMS_CONTENT_ENDPOINT)
        albums = {album["Id"]: album["Title"] for album in data.get("value", [])}
        logger.info(f"Found {len(albums)} albums")
        return albums
    except Exception as e:
        logger.error(f"Error retrieving albums: {str(e)}")
        return {} 