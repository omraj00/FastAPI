from app.db import SessionLocal
from app.models import PageView
from app.celery import celery_app

import logging
logger = logging.getLogger(__name__)

@celery_app.task()
def saving_to_db(data: dict):
    logger.info("Data saving to database: %s" % str(data))
    db = SessionLocal()
    try:
        db_pageview = PageView(
            tenant_id=data["tenant_id"],
            meta_data=data["meta_data"],
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
        print(f"Error saving user journey in database: {e}")
        db.rollback()
        return False
    finally:
        db.close()


@celery_app.task()
def saving_to_s3(data: dict):
    logger.info("Data saving to amazons3: %s" % str(data))
    return True