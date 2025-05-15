"""
HTTP client utilities for making API requests
"""
import logging
import os
import json
from typing import Dict, Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from tahubu_sf.config.settings import DEFAULT_HEADERS, AUTH_TYPE, USERNAME, PASSWORD, ENDPOINTS

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
    Get an authentication token from Sitefinity.
    
    Returns:
        Dict[str, str]: Headers with the authentication token
    """
    global _AUTH_TOKEN, _AUTH_HEADERS
    
    # If we already have a token, return the cached headers
    if _AUTH_TOKEN and _AUTH_HEADERS:
        return _AUTH_HEADERS
        
    # If anonymous, no token needed
    if AUTH_TYPE == "anonymous":
        return {}
        
    # If API key auth, headers are already set in DEFAULT_HEADERS
    if AUTH_TYPE == "apikey":
        return {}
    
    # For authenticated and administrator authentication, we need to get a token
    if AUTH_TYPE in ["authenticated", "administrator"]:
        if not USERNAME or not PASSWORD:
            logger.warning("Authentication required but username/password not provided")
            return {}
            
        try:
            # Get a token from Sitefinity
            async with httpx.AsyncClient() as client:
                data = {
                    "username": USERNAME,
                    "password": PASSWORD,
                    "grant_type": "password",
                    "scope": "openid",
                    "client_id": "sitefinity",
                }
                
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                
                logger.debug(f"Getting authentication token for user: {USERNAME}")
                response = await client.post(
                    ENDPOINTS["login"],
                    data=data,
                    headers=headers
                )
                response.raise_for_status()
                
                auth_data = response.json()
                _AUTH_TOKEN = auth_data.get("access_token")
                
                if _AUTH_TOKEN:
                    _AUTH_HEADERS = {"Authorization": f"Bearer {_AUTH_TOKEN}"}
                    logger.info("Successfully obtained authentication token")
                    return _AUTH_HEADERS
                else:
                    logger.error("Failed to get valid authentication token")
                    return {}
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during authentication: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return {}
    
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
    
    # Add authentication if needed
    if AUTH_TYPE != "anonymous":
        if AUTH_TYPE == "apikey":
            # API key is already in DEFAULT_HEADERS
            pass
        elif AUTH_TYPE in ["authenticated", "administrator"]:
            # Get token and add to headers
            auth_headers = await get_auth_token()
            request_headers.update(auth_headers)
    
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