from sqlalchemy import Column, Integer, String, Boolean
from app.database.base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    """
    Organization model - represents a tenant in the multi-tenant system.
    
    Each organization is a separate tenant with isolated data.
    Users belong to organizations through user_organizations table.
    """
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
