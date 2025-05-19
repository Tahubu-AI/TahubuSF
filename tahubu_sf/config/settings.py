"""
Configuration settings for Sitefinity API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Base URL Configuration
SITEFINITY_SITE_PREFIX = os.getenv("SITEFINITY_SITE_PREFIX", "https://thetrainingboss.com")

# Authentication Configuration
AUTH_TYPE = os.getenv("SITEFINITY_AUTH_TYPE", "anonymous").lower()
API_KEY = os.getenv("SITEFINITY_API_KEY", None)
AUTH_KEY = os.getenv("SITEFINITY_AUTH_KEY", None)
USERNAME = os.getenv("SITEFINITY_USERNAME", None)
PASSWORD = os.getenv("SITEFINITY_PASSWORD", None)

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
    # Authentication endpoints
    "login": f"{SITEFINITY_SITE_PREFIX}/Sitefinity/Authenticate/OpenID/connect/token",
}

# HTTP Headers
DEFAULT_HEADERS = {"Content-Type": "application/json"}
if AUTH_TYPE == "apikey" and API_KEY:
    DEFAULT_HEADERS["X-SF-APIKEY"] = API_KEY
elif AUTH_TYPE == "accesskey" and AUTH_KEY:
    DEFAULT_HEADERS["X-SF-Access-Key"] = AUTH_KEY

# Application settings
APP_NAME = "TahubuSFAPI" 