from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime


Base = declarative_base()


class TimestampMixin:
    """
    Mixin to add created_at and updated_at timestamps to models.
    Automatically tracks when records are created and modified.
    """
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TenantMixin:
    """
    Mixin to add organization_id (tenant_id) to models.
    
    CRITICAL for multi-tenant isolation:
    - Every tenant-scoped table must include this mixin
    - All queries must filter by organization_id
    - Prevents cross-tenant data access
    """
    organization_id = Column(Integer, nullable=False, index=True)
