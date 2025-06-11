#!/usr/bin/env python3
"""
FastMCP 2.0 Configuration
Settings for HTTP streaming transport, authentication, and proxy server capabilities
"""
import os
from typing import Optional, List
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class FastMCPConfig:
    """FastMCP 2.0 server configuration"""
    
    # Server settings
    name: str = "TahubuSF FastMCP 2.0"
    version: str = "2.0.0"
    host: str = "127.0.0.1"
    port: int = 3000
    
    # Transport settings
    transport: str = "http"  # "stdio" or "http"
    enable_streaming: bool = True
    stream_chunk_size: int = 1024
    
    # Authentication settings
    enable_auth: bool = False
    auth_type: str = "bearer"  # "bearer", "apikey", "basic"
    auth_token: Optional[str] = None
    auth_header: str = "Authorization"
    
    # Proxy settings
    enable_proxy: bool = False
    proxy_servers: List[str] = None
    proxy_timeout: int = 30
    
    # CORS settings for HTTP transport
    enable_cors: bool = True
    cors_origins: List[str] = None
    cors_methods: List[str] = None
    cors_headers: List[str] = None
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    enable_request_logging: bool = True
    
    # Rate limiting
    enable_rate_limiting: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    # Health check settings
    enable_health_check: bool = True
    health_check_path: str = "/health"
    
    # Tool settings
    tool_timeout: int = 300  # seconds
    max_tool_concurrency: int = 10
    
    def __post_init__(self):
        """Initialize default values and load from environment"""
        # Load from environment variables
        self.host = os.getenv("FASTMCP_HOST", self.host)
        self.port = int(os.getenv("FASTMCP_PORT", self.port))
        self.transport = os.getenv("FASTMCP_TRANSPORT", self.transport)
        
        # Authentication from environment
        if os.getenv("FASTMCP_ENABLE_AUTH", "").lower() == "true":
            self.enable_auth = True
        self.auth_token = os.getenv("FASTMCP_AUTH_TOKEN") or self.auth_token
        
        # Set default CORS origins if not specified
        if self.cors_origins is None:
            self.cors_origins = [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:8000",  # FastAPI server
                "http://127.0.0.1:8000"
            ]
        
        if self.cors_methods is None:
            self.cors_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        
        if self.cors_headers is None:
            self.cors_headers = [
                "Content-Type",
                "Authorization",
                "X-Requested-With",
                "Accept",
                "Origin"
            ]
        
        if self.proxy_servers is None:
            self.proxy_servers = []

# Global configuration instance
config = FastMCPConfig()

# FastMCP 2.0 advanced feature configurations
@dataclass
class StreamingConfig:
    """HTTP streaming configuration"""
    enable_server_sent_events: bool = True
    sse_heartbeat_interval: int = 30  # seconds
    sse_retry_interval: int = 3000  # milliseconds
    enable_websocket: bool = False  # Future enhancement
    websocket_path: str = "/ws"

@dataclass
class AuthConfig:
    """Authentication configuration"""
    token_expiry: int = 3600  # seconds
    refresh_token_expiry: int = 86400  # seconds
    jwt_secret: Optional[str] = None
    jwt_algorithm: str = "HS256"
    
    def __post_init__(self):
        self.jwt_secret = os.getenv("FASTMCP_JWT_SECRET") or self.jwt_secret

@dataclass
class ProxyConfig:
    """Proxy server configuration"""
    enable_load_balancing: bool = False
    load_balance_method: str = "round_robin"  # "round_robin", "random", "weighted"
    health_check_interval: int = 30  # seconds
    retry_attempts: int = 3
    retry_delay: float = 1.0  # seconds

# Feature configurations
streaming_config = StreamingConfig()
auth_config = AuthConfig()
proxy_config = ProxyConfig()

def get_server_info() -> dict:
    """Get server information for health checks and discovery"""
    return {
        "name": config.name,
        "version": config.version,
        "transport": config.transport,
        "features": {
            "streaming": config.enable_streaming,
            "authentication": config.enable_auth,
            "proxy": config.enable_proxy,
            "cors": config.enable_cors,
            "rate_limiting": config.enable_rate_limiting
        },
        "endpoints": {
            "health": config.health_check_path,
            "tools": "/tools",
            "call_tool": "/call-tool",
            "streaming": "/stream" if config.enable_streaming else None
        }
    }

def validate_config() -> List[str]:
    """Validate configuration and return any errors"""
    errors = []
    
    if config.port < 1 or config.port > 65535:
        errors.append(f"Invalid port: {config.port}")
    
    if config.enable_auth and not config.auth_token:
        errors.append("Authentication enabled but no auth token provided")
    
    if config.enable_proxy and not config.proxy_servers:
        errors.append("Proxy enabled but no proxy servers configured")
    
    if config.transport not in ["stdio", "http"]:
        errors.append(f"Invalid transport: {config.transport}")
    
    return errors

def load_config_from_file(file_path: str) -> FastMCPConfig:
    """Load configuration from a file (JSON/YAML)"""
    # This would implement loading from external config files
    # For now, return the default config
    return config 