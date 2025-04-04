from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent / "static"),
    name="static",
)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)
