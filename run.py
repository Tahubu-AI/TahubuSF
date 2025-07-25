#!/usr/bin/env python
"""
Entry point for running the TahubuSF MCP server with STDIO transport
For HTTP/web access, use the FastAPI server in fastapi_server/
"""
import argparse
import logging
import os

from tahubu_sf.app import create_app

logger = logging.getLogger(__name__)

# Create the MCP server object with a standard variable name for mcp dev to find
mcp = create_app()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run the TahubuSF MCP server")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_args()
    
    # Configure logging based on verbosity
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    logger.info("Creating TahubuSF MCP server")
    logger.info("Using STDIO transport for Claude Desktop integration")
    logger.info("For HTTP/web access, use: cd fastapi_server && python run.py")
    
    # Run the MCP server with STDIO transport (optimal for Claude Desktop)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main() 