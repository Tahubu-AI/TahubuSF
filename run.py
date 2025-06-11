#!/usr/bin/env python
"""
Entry point for running the TahubuSF MCP server
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
    parser.add_argument(
        "--transport", "-t", 
        choices=["stdio", "streamable-http"], 
        default="stdio",
        help="Transport protocol to use (default: stdio)"
    )
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host to bind to for HTTP transport (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", "-p", 
        type=int, 
        default=5000,
        help="Port to bind to for HTTP transport (default: 5000)"
    )
    parser.add_argument(
        "--path",
        default="/mcp",
        help="Path for HTTP transport (default: /mcp)"
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
    
    if args.transport == "stdio":
        logger.info("To run in development mode with web interface, use: python simple_server.py")
        logger.info("Starting in production mode (stdio only)")
        # Run the MCP server with stdio transport
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        logger.info(f"Starting HTTP server on {args.host}:{args.port}{args.path}")
        # Run the MCP server with streamable HTTP transport (recommended for web deployments)
        mcp.run(transport="streamable-http", host=args.host, port=args.port, path=args.path)

if __name__ == "__main__":
    main() 