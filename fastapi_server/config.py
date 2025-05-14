"""
Configuration settings for the FastAPI server
"""
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseModel):
    """FastAPI server settings"""
    # API Settings
    API_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = int(os.environ.get("PORT", 8000))
    LOG_LEVEL: str = "info"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]  # For production, specify exact domains
    
    # Media Settings
    MEDIA_DIR: str = os.path.join(BASE_DIR, "media")
    
    # UI Settings
    UI_HTML_PATH: str = os.path.join(BASE_DIR, "inspector.html")
    
    # Azure Settings
    AZURE_APP_NAME: Optional[str] = os.environ.get("AZURE_APP_NAME", None)
    APPINSIGHTS_KEY: Optional[str] = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY", None)
    
    # Retry Settings
    RETRY_MAX_ATTEMPTS: int = int(os.environ.get("RETRY_MAX_ATTEMPTS", 3))
    RETRY_MIN_SECONDS: float = float(os.environ.get("RETRY_MIN_SECONDS", 1))
    RETRY_MAX_SECONDS: float = float(os.environ.get("RETRY_MAX_SECONDS", 10))

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"

# Load settings
settings = Settings()