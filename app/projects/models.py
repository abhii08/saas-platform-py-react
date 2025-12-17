from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from app.database.base import Base, TimestampMixin, TenantMixin


class Project(Base, TimestampMixin, TenantMixin):
    """
    Project model - represents a project within an organization.
    
    Multi-tenant isolation:
    - Includes organization_id (via TenantMixin)
    - All queries must filter by organization_id
    - Projects are scoped to a single organization
    """
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    slug = Column(String(100), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
