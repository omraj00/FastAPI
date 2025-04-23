from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class PageViewBase(BaseModel):
    meta_data: dict
    session_id: str
    page_url: str
    tenant_id: int

    @field_validator("meta_data")
    def check_identityid(cls, values):
        if "identityid" not in values:
            raise ValueError("meta_data must include 'identityid'")
        return values
    
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


class StorageCategory(str, Enum):
    database = "database"
    amazons3 = "amazons3"
    both = "both"

class TenantBase(BaseModel):
    name: str
    domain: str
    storage_type: StorageCategory 
    is_active: bool

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None
    storage_type: Optional[StorageCategory] = None

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

class TenantResponse(BaseModel):
    tenant: str
    tenant_id: int
    is_active: bool