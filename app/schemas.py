from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PageViewBase(BaseModel):
    identity_id: Optional[str] = None
    session_id: str
    page_url: str
    tenant_id: int


class PageViewCreate(PageViewBase):
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


class PageViewInDB(PageViewBase):
    id: int
    timestamp: datetime
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True


class PageView(PageViewInDB):
    pass


class TenantBase(BaseModel):
    name: str
    domain: str


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None


class TenantInDB(TenantBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Tenant(TenantInDB):
    pass


class TrackResponse(BaseModel):
    message: str
    status: str