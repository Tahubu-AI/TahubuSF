"""
API endpoints for creating and managing events
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request, make_post_request
from tahubu_sf.utils import generate_url_name

logger = logging.getLogger(__name__)

CALENDARS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.calendars}"
EVENTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.events}"
EVENTS_MANAGEMENT_ENDPOINT = f"{ENDPOINTS.management}/{CONTENT_TYPES.events}"

async def create_event(
    title: str,
    summary: str,
    content: str,
    eventstart: datetime,
    eventend: datetime,
    parent_id: str,
    draft: bool = True,
) -> Dict[str, Any]:
    """
    Create a new event as a draft in Sitefinity.
    
    Args:
        title: The title of the event (REQUIRED)
        summary: A brief summary of the event (REQUIRED)
        content: The main content of the event (HTML supported)
        eventstart: The start date and time of the event
        eventend: The end date and time of the event
        parent_id: The ID of the parent calendar (REQUIRED)
        draft: Whether to create the event as a draft (default: True)
    
    Returns:
        Dict[str, Any]: Response from the Sitefinity API, including the created event's ID
    """
    try:
        logger.info(f"Creating event draft with title: {title}")
        
        # Validate required parameters
        if not parent_id:
            raise ValueError("Parent event ID (parent_id) is required for creating events")
        
        # Create a timestamp for the current time
        now = datetime.utcnow().isoformat() + "Z"
        
        # Prepare the event data
        post_data = {
            "Title": title,
            "Summary": summary,
            "Content": content,
            "EventStart": eventstart.isoformat() + "Z",
            "EventEnd": eventend.isoformat() + "Z",
            "ParentId": parent_id,
        }
        
        # Generate a proper URL name from the title following Sitefinity requirements
        url_name = generate_url_name(title)
        
        post_data["UrlName"] = url_name
        
        logger.debug(f"Generated URL name: {url_name}")

        endpoint = EVENTS_MANAGEMENT_ENDPOINT if draft else EVENTS_CONTENT_ENDPOINT
        
        # Send POST request to create the Event
        response = await make_post_request(endpoint, post_data)
        
        logger.info(f"Event draft created successfully: {response.get('Id', 'unknown ID')}")
        return response
    except Exception as e:
        logger.error(f"Error creating Event draft: {str(e)}")
        raise Exception(f"Failed to create Event draft: {str(e)}") from e

async def get_calendars() -> Dict[str, str]:
    """
    Get a list of available parent calendars for selection.
    
    Returns:
        Dict[str, str]: Dictionary of calendar IDs and their titles
    """
    try:
        data = await make_request(CALENDARS_CONTENT_ENDPOINT)
        calendars = {calendar["Id"]: calendar["Title"] for calendar in data.get("value", [])}
        logger.info(f"Found {len(calendars)} parent calendars")
        return calendars
    except Exception as e:
        logger.error(f"Error retrieving parent calendars: {str(e)}")
        return {} 