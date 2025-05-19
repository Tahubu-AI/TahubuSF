"""
HTTP client utilities for making API requests
"""
import logging
import os
import json
from typing import Dict, Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from tahubu_sf.config.settings import DEFAULT_HEADERS, AUTH_TYPE, AUTH_KEY, API_KEY, ENDPOINTS

logger = logging.getLogger(__name__)

# Get retry configuration from environment variables
MAX_RETRIES = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
MIN_WAIT = float(os.getenv("RETRY_MIN_SECONDS", "1"))
MAX_WAIT = float(os.getenv("RETRY_MAX_SECONDS", "5"))

logger.debug(f"Initialized retry configuration: MAX_ATTEMPTS={MAX_RETRIES}, MIN_WAIT={MIN_WAIT}s, MAX_WAIT={MAX_WAIT}s")
logger.debug(f"Authentication type: {AUTH_TYPE}")

# Cache for the authentication token
_AUTH_TOKEN = None
_AUTH_HEADERS = {}

async def get_auth_token() -> Dict[str, str]:
    """
    Get authentication headers for Sitefinity API.
    
    Returns:
        Dict[str, str]: Headers with the authentication information
    """
    # For anonymous, apikey, and accesskey types, the headers are already set in DEFAULT_HEADERS
    # No additional token generation needed
    if AUTH_TYPE == "anonymous":
        logger.debug("Using anonymous authentication")
        return {}
    
    if AUTH_TYPE == "apikey":
        if not API_KEY:
            logger.warning("API key authentication configured but no API key provided")
            return {}
        logger.debug("Using API key authentication")
        return {"X-SF-APIKEY": API_KEY}
    
    if AUTH_TYPE == "accesskey" or AUTH_TYPE == "authenticated":  # Support both names
        if not AUTH_KEY:
            logger.warning("Access key authentication configured but no access key provided")
            return {}
        logger.debug("Using Access Key authentication")
        return {"X-SF-Access-Key": AUTH_KEY}
    
    logger.warning(f"Unsupported authentication type: {AUTH_TYPE}")
    return {}

@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=MIN_WAIT, max=MAX_WAIT),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
    reraise=True,
    before_sleep=lambda retry_state: logger.warning(
        f"Retry attempt {retry_state.attempt_number}/{MAX_RETRIES} after error: {retry_state.outcome.exception()}"
    )
)
async def make_request(
    url: str, 
    headers: Optional[Dict[str, str]] = None, 
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP GET request to the specified URL with automatic retries for transient errors.
    Will include authentication headers if configured.
    
    Args:
        url: The URL to make the request to
        headers: Optional headers to include in the request
        params: Optional query parameters
        
    Returns:
        The JSON response as a dictionary
        
    Raises:
        httpx.HTTPStatusError: If the request fails after all retry attempts
    """
    # Start with default headers
    request_headers = dict(DEFAULT_HEADERS)
    
    # Add any custom headers
    if headers:
        request_headers.update(headers)
    
    # Add authentication headers if needed (headers from DEFAULT_HEADERS might be overwritten here)
    auth_headers = await get_auth_token()
    if auth_headers:
        request_headers.update(auth_headers)
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Making GET request to {url}")
            logger.debug(f"Request headers: {request_headers}")
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

@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=MIN_WAIT, max=MAX_WAIT),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
    reraise=True,
    before_sleep=lambda retry_state: logger.warning(
        f"Retry attempt {retry_state.attempt_number}/{MAX_RETRIES} after error: {retry_state.outcome.exception()}"
    )
)
async def make_post_request(
    url: str,
    data: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP POST request to the specified URL with automatic retries for transient errors.
    Will include authentication headers if configured.
    
    Args:
        url: The URL to make the request to
        data: The JSON data to send in the request body
        headers: Optional headers to include in the request
        
    Returns:
        The JSON response as a dictionary
        
    Raises:
        httpx.HTTPStatusError: If the request fails after all retry attempts
    """
    # Start with default headers
    request_headers = dict(DEFAULT_HEADERS)
    
    # Add any custom headers
    if headers:
        request_headers.update(headers)
    
    # Add authentication headers if needed
    auth_headers = await get_auth_token()
    if auth_headers:
        request_headers.update(auth_headers)
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Making POST request to {url}")
            logger.debug(f"Request headers: {request_headers}")
            logger.debug(f"Request data: {data}")
            
            response = await client.post(
                url, 
                json=data, 
                headers=request_headers
            )
            response.raise_for_status()
            
            # Some POST responses may not include JSON content
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            else:
                logger.debug(f"Response status: {response.status_code}")
                return {"status": "success", "status_code": response.status_code}
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        logger.error(f"Response content: {e.response.content.decode() if hasattr(e, 'response') else 'No response'}")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise