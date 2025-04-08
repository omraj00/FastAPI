import uvicorn
from app.config import settings
from app.server import app

if __name__ == "__main__":

    print("Celery Broker:", settings.CELERY_BROKER_URL)
    print("Celery Broker:", settings.CELERY_RESULT_BACKEND)

    uvicorn.run(
        "app.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE
    )
