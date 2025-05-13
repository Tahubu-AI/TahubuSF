"""
HTTP client utilities for making API requests
"""
import logging
from typing import Dict, Any, Optional

import httpx

from tahubu_sf.config.settings import DEFAULT_HEADERS

logger = logging.getLogger(__name__)

async def make_request(
    url: str, 
    headers: Optional[Dict[str, str]] = None, 
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP GET request to the specified URL.
    
    Args:
        url: The URL to make the request to
        headers: Optional headers to include in the request
        params: Optional query parameters
        
    Returns:
        The JSON response as a dictionary
        
    Raises:
        httpx.HTTPStatusError: If the request fails
    """
    request_headers = headers or DEFAULT_HEADERS
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Making request to {url}")
            response = await client.get(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise 