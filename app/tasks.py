from app.db import SessionLocal
from app.models import PageView
from app.celery import celery_app

@celery_app.task()
def save_user_journey(data: dict):
    db = SessionLocal()
    try:
        db_pageview = PageView(
            tenant_id=data["tenant_id"],
            identity_id=data["identity_id"],
            session_id=data["session_id"],
            page_url=data["page_url"],
            user_agent=data["user_agent"],
            ip_address=data["ip_address"]
        )
        db.add(db_pageview)
        db.commit()
        db.refresh(db_pageview)
        return True
    except Exception as e:
        print(f"Error saving user journey in Celery task: {e}")
        db.rollback()
        return False
    finally:
        db.close()
