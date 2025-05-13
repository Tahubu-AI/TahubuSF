#!/usr/bin/env python
"""
Entry point script to run the FastAPI server for TahubuSF
"""
import argparse
import logging
import os
import sys

# Use relative import when run directly from fastapi_server directory
try:
    from fastapi_server.main import start as start_server
    from fastapi_server.config import settings
except ModuleNotFoundError:
    # Fallback to relative imports when run directly from this directory
    from .main import start as start_server
    from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("tahubu_sf")

def main():
    """Parse command line arguments and start the server"""
    parser = argparse.ArgumentParser(description="Run the TahubuSF FastAPI server")
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=settings.PORT,
        help=f"Port to run the server on (default: {settings.PORT})"
    )
    
    parser.add_argument(
        "--host", 
        type=str, 
        default=settings.HOST,
        help=f"Host to bind to (default: {settings.HOST})"
    )
    
    parser.add_argument(
        "--log-level", 
        type=str, 
        default=settings.LOG_LEVEL,
        choices=["debug", "info", "warning", "error", "critical"],
        help=f"Logging level (default: {settings.LOG_LEVEL})"
    )
    
    args = parser.parse_args()
    
    # Update settings from command line arguments
    settings.PORT = args.port
    settings.HOST = args.host
    settings.LOG_LEVEL = args.log_level
    
    logger.info(f"Starting TahubuSF FastAPI server on {settings.HOST}:{settings.PORT}")
    
    try:
        start_server()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 