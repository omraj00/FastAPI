from pydantic import BaseModel
import os
from pathlib import Path


class Settings(BaseModel):
    # Base settings
    PROJECT_NAME: str = "MultiTenant Blog Tracker"
    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API settings
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./fastapi_blog_tracker.db"
    
    # Templates
    TEMPLATES_DIR: Path = Path(__file__).parent.parent / "templates"

    # Security
    SECRET_KEY: str = "supersecretkey"  # In production, use a proper secure key
    
    class Config:
        env_file = ".env"


settings = Settings()
