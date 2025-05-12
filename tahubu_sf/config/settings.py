"""
Configuration settings for Sitefinity API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Base URL Configuration
SITEFINITY_SITE_PREFIX = os.getenv("SITEFINITY_SITE_PREFIX", "https://thetrainingboss.com")

# API Endpoints
ENDPOINTS = {
    "news": f"{SITEFINITY_SITE_PREFIX}/api/default/newsitems",
    "blogs": f"{SITEFINITY_SITE_PREFIX}/api/default/blogs",
    "blog_posts": f"{SITEFINITY_SITE_PREFIX}/api/default/blogposts",
    "events": f"{SITEFINITY_SITE_PREFIX}/api/default/eventsitems",
    "sites": f"{SITEFINITY_SITE_PREFIX}/api/default/sites",
    "lists": f"{SITEFINITY_SITE_PREFIX}/api/default/lists",
    "list_items": f"{SITEFINITY_SITE_PREFIX}/api/default/listitems",
    "shared_content": f"{SITEFINITY_SITE_PREFIX}/api/default/contentitems",
    "pages": f"{SITEFINITY_SITE_PREFIX}/api/default/pages",
    "page_templates": f"{SITEFINITY_SITE_PREFIX}/api/default/templates",
}

# HTTP Headers
DEFAULT_HEADERS = {"Content-Type": "application/json"}

# Application settings
APP_NAME = "TahubuSFAPI" 