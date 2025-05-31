"""
API endpoints for creating and managing list items
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request, make_post_request

logger = logging.getLogger(__name__)

LISTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.lists}"
LISTITEMS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.list_items}"
LISTITEMS_MANAGEMENT_ENDPOINT = f"{ENDPOINTS.management}/{CONTENT_TYPES.list_items}"

async def create_list_item(
    title: str,
    content: str,
    parent_id: str,
    draft: bool = True,
) -> Dict[str, Any]:
    """
    Create a new list item as a draft in Sitefinity.
    
    Args:
        title: The title of the list item (REQUIRED)
        content: The main content of the list item (HTML supported)
        parent_id: The ID of the parent list (REQUIRED)
        draft: Whether to create the list item as a draft (default: True)
    
    Returns:
        Dict[str, Any]: Response from the Sitefinity API, including the created list item's ID
    """
    try:
        logger.info(f"Creating list item draft with title: {title}")
        
        # Validate required parameters
        if not parent_id:
            raise ValueError("Parent list ID (parent_id) is required for creating list items")
        
        # Create a timestamp for the current time
        now = datetime.utcnow().isoformat() + "Z"
        
        # Prepare the list item data
        post_data = {
            "Title": title,
            "Content": content,
            "PublicationDate": now,
            "ParentId": parent_id,
        }
        
        # Generate a proper URL name from the title following Sitefinity requirements
        # - Remove any non-alphanumeric characters except hyphens
        # - Convert to lowercase
        # - Replace spaces and other characters with hyphens
        # - Remove consecutive hyphens
        # - Remove leading/trailing hyphens
        # - Limit to 100 characters
        url_name = title.lower()
        # First replace spaces with hyphens
        url_name = url_name.replace(" ", "-")
        # Then replace all non-alphanumeric and non-hyphen characters
        url_name = re.sub(r'[^a-z0-9-]', '', url_name)
        # Replace multiple consecutive hyphens with a single one
        url_name = re.sub(r'-+', '-', url_name)
        # Remove leading/trailing hyphens
        url_name = url_name.strip('-')
        # Limit to 100 characters
        url_name = url_name[:100]
        
        post_data["UrlName"] = url_name
        
        logger.debug(f"Generated URL name: {url_name}")

        endpoint = LISTITEMS_MANAGEMENT_ENDPOINT if draft else LISTITEMS_CONTENT_ENDPOINT
        
        # Send POST request to create the List Item
        response = await make_post_request(endpoint, post_data)
        
        logger.info(f"List Item draft created successfully: {response.get('Id', 'unknown ID')}")
        return response
    except Exception as e:
        logger.error(f"Error creating List Item draft: {str(e)}")
        raise Exception(f"Failed to create List Item draft: {str(e)}") from e

async def get_parent_Lists() -> Dict[str, str]:
    """
    Get a list of available parent lists for selection.
    
    Returns:
        Dict[str, str]: Dictionary of Lists IDs and their titles
    """
    try:
        data = await make_request(LISTS_CONTENT_ENDPOINT)
        lists = {list["Id"]: list["Title"] for list in data.get("value", [])}
        logger.info(f"Found {len(lists)} parent lists")
        return lists
    except Exception as e:
        logger.error(f"Error retrieving parent lists: {str(e)}")
        return {} 