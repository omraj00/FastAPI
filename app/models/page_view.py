from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


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
