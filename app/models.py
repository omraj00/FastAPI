from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.db import Base


class PageView(Base):
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    identity_id = Column(String, index=True)
    session_id = Column(String, index=True)
    page_url = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())