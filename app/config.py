from pydantic import BaseModel
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
    TEMPLATES_DIR: Path = Path(__file__).parent / "static"

    # Security
    SECRET_KEY: str = "supersecretkey"  # In production, use a proper secure key

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"


settings = Settings()
