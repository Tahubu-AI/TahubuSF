#!/usr/bin/env python3
"""
FastMCP 2.0 Package
Advanced HTTP Streaming Transport Protocol for TahubuSF MCP Tools

This package provides FastMCP 2.0 implementation with:
- HTTP streaming transport
- Authentication and security
- Remote server proxying
- Client library
- Production-ready features

Usage:
    # Basic server
    from fastmcp.server import create_fastmcp_server
    server = create_fastmcp_server()
    server.run(transport="http")
    
    # Client
    from fastmcp.client import TahubuSFClient
    client = TahubuSFClient("http://127.0.0.1:3000")
    await client.connect()
    
    # Configuration
    from fastmcp.config import config
    config.enable_auth = True
"""

from .server import create_fastmcp_server
from .client import TahubuSFClient
from .config import config, streaming_config, auth_config, proxy_config

__version__ = "2.0.0"
__author__ = "TahubuSF Team"
__description__ = "FastMCP 2.0 HTTP Streaming Transport Protocol"

# Package metadata
__all__ = [
    "create_fastmcp_server",
    "TahubuSFClient", 
    "config",
    "streaming_config",
    "auth_config",
    "proxy_config"
]

# FastMCP 2.0 feature flags
FEATURES = {
    "http_streaming": True,
    "authentication": True,
    "remote_proxy": True,
    "client_library": True,
    "server_composition": True,
    "cors_support": True,
    "rate_limiting": True,
    "health_checks": True,
    "production_ready": True
}

def get_version():
    """Get package version"""
    return __version__

def get_features():
    """Get available features"""
    return FEATURES.copy()

def print_info():
    """Print package information"""
    print(f"FastMCP {__version__}")
    print(f"Description: {__description__}")
    print("\nFeatures:")
    for feature, enabled in FEATURES.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature.replace('_', ' ').title()}")
    print(f"\nComponents:")
    print(f"  • Server: fastmcp.server")
    print(f"  • Client: fastmcp.client") 
    print(f"  • Config: fastmcp.config")
    print(f"  • Tests: fastmcp.test_fastmcp")

# Development and debugging helpers
def validate_installation():
    """Validate FastMCP 2.0 installation"""
    import importlib
    
    required_modules = [
        "fastmcp",
        "httpx", 
        "asyncio",
        "logging"
    ]
    
    missing = []
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing required modules: {', '.join(missing)}")
        return False
    else:
        print("✅ FastMCP 2.0 installation validated")
        return True

if __name__ == "__main__":
    print_info()
    validate_installation() 