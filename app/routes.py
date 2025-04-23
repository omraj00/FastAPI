from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from uuid import uuid4
from app.db import get_db
from app.config import settings
from app.models import Tenant, StorageCategory
from app.tasks import saving_to_db, saving_to_s3
from app.schemas import TrackResponse, PageViewCreate, TenantCreate, TenantResponse, Tenant as TenantSchema

import logging
router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


# Helper function to get tenant based on domain
@router.get("/get-tenant-id", response_model=TenantResponse)
def get_tenant_by_domain(domain: str, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.domain == domain).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if not tenant.is_active:
        raise HTTPException(status_code=400, detail="Tenant is not active")
    return {"tenant": tenant.name, "tenant_id": tenant.id, "is_active": tenant.is_active}


# Route for the blog page
@router.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request, db: Session = Depends(get_db)):

    host = request.headers.get('host', '').split(':')[0]
    session_id = request.cookies.get("session_id")
    response = templates.TemplateResponse("blog.html", {"request": request})

    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=False,                 # Change to True (bcoz True is not working on local)
            secure=False,                   # Change to True in production with HTTPS
            max_age=60 * 60 * 24 * 7        # 7 days
        )

    return response


# API endpoint to track page views
@router.post("/track-pageview", response_model=TrackResponse)
async def track_pageview(
    pageview: PageViewCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {"error": "Session ID not found in cookies"}

    try:
        tenant = db.query(Tenant).filter(Tenant.id == pageview.tenant_id).first()
    except Exception as e:
        logger.error(f"Error fetching tenant: {e}")
        tenant = None

    # Run Celery task conditionally
    if tenant: 
        if not tenant.is_active:
            raise HTTPException(status_code=400, detail="Tenant is not active")
        
        if tenant.is_active and tenant.storage_type in [StorageCategory.both, StorageCategory.database]:
            saving_to_db.delay({
                "tenant_id": pageview.tenant_id,
                "meta_data": pageview.meta_data,
                "session_id": session_id,
                "page_url": pageview.page_url,
                "user_agent": request.headers.get("user-agent"),
                "ip_address": request.client.host
            })

        if tenant.is_active and tenant.storage_type in [StorageCategory.both, StorageCategory.amazons3]:
            saving_to_s3.delay({
                "tenant_id": pageview.tenant_id,
                "meta_data": pageview.meta_data,
                "session_id": session_id,
                "page_url": pageview.page_url,
                "user_agent": request.headers.get("user-agent"),
                "ip_address": request.client.host
            })
    else:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "message": "Pageview tracking started",
        "status": "processing"
    }


# API endpoint to create a new tenant
@router.post("/tenants", response_model=TenantSchema)
async def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):
    db_tenant = Tenant(**tenant.model_dump())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


# API endpoint to get all tenants
@router.get("/tenants", response_model=List[TenantSchema])
async def get_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    return tenants
