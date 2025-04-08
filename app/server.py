from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router as api_router
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)
