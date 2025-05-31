"""
Configuration settings for Sitefinity API
"""
import os
from dotenv import load_dotenv
from types import SimpleNamespace

load_dotenv()

# Sitefinity Configuration
SITEFINITY_SITE_PREFIX = os.getenv("SITEFINITY_SITE_PREFIX").rstrip("/")
if not SITEFINITY_SITE_PREFIX or SITEFINITY_SITE_PREFIX == '':
    raise ValueError("SITEFINITY_SITE_PREFIX must be set in the environment variables.")

SITEFINITY_FRONTEND_API_PATH = os.getenv("SITEFINITY_FRONTEND_API_ROUTE", "api/default").rstrip("/").lstrip("/")
SITEFINITY_BACKEND_API_PATH = os.getenv("SITEFINITY_BACKEND_API_ROUTE", "sf/system").rstrip("/").lstrip("/")

# Authentication Configuration
AUTH_TYPE = os.getenv("SITEFINITY_AUTH_TYPE", "anonymous").lower()
API_KEY = os.getenv("SITEFINITY_API_KEY", None)
AUTH_KEY = os.getenv("SITEFINITY_AUTH_KEY", None)
USERNAME = os.getenv("SITEFINITY_USERNAME", None)
PASSWORD = os.getenv("SITEFINITY_PASSWORD", None)

ENDPOINTS = SimpleNamespace(
    content = f"{SITEFINITY_SITE_PREFIX}/{SITEFINITY_FRONTEND_API_PATH}",
    management = f"{SITEFINITY_SITE_PREFIX}/{SITEFINITY_BACKEND_API_PATH}",
    authentication = f"{SITEFINITY_SITE_PREFIX}/Sitefinity/Authenticate/OpenID/connect/token"
)

# API Endpoints
CONTENT_TYPES = SimpleNamespace(
    news = "newsitems",
    blogs = "blogs",
    blog_posts = "blogposts",
    events = "eventsitems",
    sites = "sites",
    lists = "lists",
    list_items = "listitems",
    shared_content = "contentitems",
    pages = "pages",
    page_templates = "templates",
    calendars = "calendars",
    events = "events",
    image_libraries = "albums",
    images = "images",
    document_libraries = "documentlibraries",
    documents = "documents",
    video_libraries = "videolibraries",
    videos = "videos",
    form_drafts = "form-drafts",
    forms = "forms",
    search_indexes = "searchindexes",
    pipe_settings = "pipe-settings",
    servicehooks = "servicehooks",
    classifications = "taxonomies",
    flat_taxonomies = "flat-taxa",
    Hierarchical_Taxonomies = "hierarchy-taxa",
    folders = "folders",
    section_presets = "widgetpresets"
)

# HTTP Headers
DEFAULT_HEADERS = {"Content-Type": "application/json"}
if AUTH_TYPE == "apikey" and API_KEY:
    DEFAULT_HEADERS["X-SF-APIKEY"] = API_KEY
elif AUTH_TYPE == "accesskey" and AUTH_KEY:
    DEFAULT_HEADERS["X-SF-Access-Key"] = AUTH_KEY

# Application settings
APP_NAME = "TahubuSFAPI" 