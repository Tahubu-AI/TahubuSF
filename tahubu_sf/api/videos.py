"""
API endpoints for creating and managing videos
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request, make_post_request

logger = logging.getLogger(__name__)

VIDEOLIBRARIES_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.video_libraries}"
VIDEOS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.videos}"
VIDEOS_MANAGEMENT_ENDPOINT = f"{ENDPOINTS.management}/{CONTENT_TYPES.videos}"

async def create_video(
    title: str,
    content: str,
    parent_id: str,
    draft: bool = True,
) -> Dict[str, Any]:
    """
    Upload a new video as a draft in Sitefinity.
    
    Args:
        title: The title of the video
        content: The main content of the video (HTML supported)
        parent_id: The ID of the Video Library (REQUIRED)
        draft: Whether to create the video as a draft (default: True)
    
    Returns:
        Dict[str, Any]: Response from the Sitefinity API, including the created video's ID
    """
    try:
        logger.info(f"Creating video draft with title: {title}")
        
        # Validate required parameters
        if not parent_id:
            raise ValueError("Parent Video Library ID (parent_id) is required for creating videos")
        
        # Create a timestamp for the current time
        now = datetime.utcnow().isoformat() + "Z"
        
        # Prepare the blog post data
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

        endpoint = VIDEOS_MANAGEMENT_ENDPOINT if draft else VIDEOS_CONTENT_ENDPOINT
        
        # Send POST request to create the blog post
        response = await make_post_request(endpoint, post_data)
        
        logger.info(f"Video draft created successfully: {response.get('Id', 'unknown ID')}")
        return response
    except Exception as e:
        logger.error(f"Error creating video draft: {str(e)}")
        raise Exception(f"Failed to create video draft: {str(e)}") from e

async def get_video_libraries() -> Dict[str, str]:
    """
    Get a list of available video libraries for selection.
    
    Returns:
        Dict[str, str]: Dictionary of video library IDs and their titles
    """
    try:
        data = await make_request(VIDEOLIBRARIES_CONTENT_ENDPOINT)
        vlibraries = {video["Id"]: video["Title"] for video in data.get("value", [])}
        logger.info(f"Found {len(vlibraries)} video libraries")
        return vlibraries
    except Exception as e:
        logger.error(f"Error retrieving video libraries: {str(e)}")
        return {} 