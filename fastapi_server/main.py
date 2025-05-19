#!/usr/bin/env python
"""
FastAPI server for the TahubuSF MCP tools that can be deployed to Azure App Service
"""
import os
import logging
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Add the project root to the path so imports work correctly
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from our modular architecture
from tahubu_sf.api.news import get_news
from tahubu_sf.api.blogs import get_blog_posts
from tahubu_sf.api.pages import get_pages, get_page_templates
from tahubu_sf.api.sites import get_sites
from tahubu_sf.config.settings import APP_NAME, AUTH_TYPE, API_KEY, USERNAME, AUTH_KEY

# Import local modules
from fastapi_server.routes import router
from fastapi_server.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("tahubu_sf.fastapi")

# Create FastAPI app
app = FastAPI(
    title=f"{APP_NAME} API",
    description="REST API for Sitefinity MCP tools",
    version=settings.API_VERSION,
)

# Configure CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (media directory)
app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")

# Include API routes
app.include_router(router)

# Define health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Azure App Service"""
    auth_status = {
        "type": AUTH_TYPE,
        "configured": True if (
            AUTH_TYPE == "anonymous" or
            (AUTH_TYPE == "apikey" and API_KEY) or
            (AUTH_TYPE == "accesskey" and AUTH_KEY) or
            (AUTH_TYPE == "authenticated" and AUTH_KEY)  # For backward compatibility
        ) else False
    }
    
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "authentication": auth_status
    }

# Define root endpoint to serve the UI
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Serve the UI HTML page"""
    with open(settings.UI_HTML_PATH, "r") as f:
        return f.read()

def start():
    """Start the server (used for production)"""
    logger.info(f"Starting {APP_NAME} FastAPI server on {settings.HOST}:{settings.PORT}")
    logger.info(f"Retry configuration: MAX_ATTEMPTS={settings.RETRY_MAX_ATTEMPTS}, "
               f"MIN_WAIT={settings.RETRY_MIN_SECONDS}s, "
               f"MAX_WAIT={settings.RETRY_MAX_SECONDS}s")
    logger.info(f"Sitefinity configuration: SITE_PREFIX={os.getenv('SITEFINITY_SITE_PREFIX', '')}")
    
    # Log authentication configuration
    auth_info = f"Authentication type: {AUTH_TYPE}"
    if AUTH_TYPE == "apikey":
        auth_info += f", API Key: {'configured' if API_KEY else 'not configured'}"
    elif AUTH_TYPE == "accesskey":
        auth_info += f", Auth Key: {'configured' if AUTH_KEY else 'not configured'}" 
    logger.info(auth_info)
    
    uvicorn.run(
        "fastapi_server.main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL
    )

if __name__ == "__main__":
    # This is for local development only
    logger.info(f"Starting {APP_NAME} FastAPI server on {settings.HOST}:{settings.PORT}")
    logger.info(f"Retry configuration: MAX_ATTEMPTS={settings.RETRY_MAX_ATTEMPTS}, "
               f"MIN_WAIT={settings.RETRY_MIN_SECONDS}s, "
               f"MAX_WAIT={settings.RETRY_MAX_SECONDS}s")
    logger.info(f"Sitefinity configuration: SITE_PREFIX={os.getenv('SITEFINITY_SITE_PREFIX', '')}")
    
    # Log authentication configuration
    auth_info = f"Authentication type: {AUTH_TYPE}"
    if AUTH_TYPE == "apikey":
        auth_info += f", API Key: {'configured' if API_KEY else 'not configured'}"
    elif AUTH_TYPE == "accesskey":
        auth_info += f", Auth Key: {'configured' if AUTH_KEY else 'not configured'}"
    logger.info(auth_info)
    
    start()