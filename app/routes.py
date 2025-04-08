from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from uuid import uuid4
from app.db import get_db
from app.models import Tenant
from app.config import settings
from app.tasks import save_user_journey
from app.schemas import TrackResponse, PageViewCreate, TenantCreate, Tenant as TenantSchema

router = APIRouter()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


# Helper function to get tenant based on domain
def get_tenant_by_domain(domain: str, db: Session):
    tenant = db.query(Tenant).filter(Tenant.domain == domain).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


# Route for the blog page
@router.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request, db: Session = Depends(get_db)):

    host = request.headers.get('host', '').split(':')[0]
    session_id = request.cookies.get("session_id")
    try:
        tenant = get_tenant_by_domain(host, db)
    except HTTPException:
        tenant = None

    response = templates.TemplateResponse(
        "blog.html",
        {"request": request, "tenant": tenant}
    )

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
    # db: Session = Depends(get_db)
):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {"error": "Session ID not found in cookies"}
    # print("Session ID: ", session_id)

    # Run Celery task
    save_user_journey.delay({
        "tenant_id": pageview.tenant_id,
        "identity_id": pageview.identity_id,
        "session_id": session_id,
        "page_url": pageview.page_url,
        "user_agent": request.headers.get("user-agent"),
        "ip_address": request.client.host
    })

    # print("Session ID 2: ", session_id)
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
    db_tenant = Tenant(**tenant.dict())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


# API endpoint to get all tenants
@router.get("/tenants", response_model=List[TenantSchema])
async def get_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    return tenants
