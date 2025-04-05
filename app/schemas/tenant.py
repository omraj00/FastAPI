from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
