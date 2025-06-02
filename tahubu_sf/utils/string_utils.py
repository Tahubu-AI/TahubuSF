"""
String utility functions for Tahubu Sitefinity
"""
import re
from typing import Optional


def generate_url_name(title: str, max_length: int = 100) -> str:
    """
    Generate a proper URL name from a title following Sitefinity requirements:
    - Convert to lowercase
    - Replace spaces with hyphens
    - Remove any non-alphanumeric characters except hyphens
    - Replace multiple consecutive hyphens with a single one
    - Remove leading/trailing hyphens
    - Limit to specified max length (default: 100 characters)
    
    Args:
        title: The title to convert to a URL name
        max_length: Maximum length of the URL name (default: 100)
        
    Returns:
        str: A URL-friendly name
    """
    url_name = title.lower()
    # First replace spaces with hyphens
    url_name = url_name.replace(" ", "-")
    # Then replace all non-alphanumeric and non-hyphen characters
    url_name = re.sub(r'[^a-z0-9-]', '', url_name)
    # Replace multiple consecutive hyphens with a single one
    url_name = re.sub(r'-+', '-', url_name)
    # Remove leading/trailing hyphens
    url_name = url_name.strip('-')
    # Limit to max_length characters
    url_name = url_name[:max_length]
    
    return url_name 