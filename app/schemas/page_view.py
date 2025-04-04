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
        orm_mode = True


class PageView(PageViewInDB):
    pass
