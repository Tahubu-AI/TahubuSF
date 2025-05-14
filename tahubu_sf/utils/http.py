"""
HTTP client utilities for making API requests
"""
import logging
import os
from typing import Dict, Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from tahubu_sf.config.settings import DEFAULT_HEADERS

logger = logging.getLogger(__name__)

# Get retry configuration from environment variables
MAX_RETRIES = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
MIN_WAIT = float(os.getenv("RETRY_MIN_SECONDS", "1"))
MAX_WAIT = float(os.getenv("RETRY_MAX_SECONDS", "10"))

logger.debug(f"Initialized retry configuration: MAX_ATTEMPTS={MAX_RETRIES}, MIN_WAIT={MIN_WAIT}s, MAX_WAIT={MAX_WAIT}s")

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
    
    Args:
        url: The URL to make the request to
        headers: Optional headers to include in the request
        params: Optional query parameters
        
    Returns:
        The JSON response as a dictionary
        
    Raises:
        httpx.HTTPStatusError: If the request fails after all retry attempts
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