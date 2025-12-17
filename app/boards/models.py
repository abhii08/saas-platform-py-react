from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database.base import Base, TimestampMixin, TenantMixin


class Board(Base, TimestampMixin, TenantMixin):
    """
    Board model - represents a board within a project (e.g., Kanban board).
    
    Multi-tenant isolation:
    - Includes organization_id (via TenantMixin)
    - Belongs to a project which is also tenant-scoped
    - Double isolation: project_id AND organization_id
    """
    __tablename__ = "boards"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    position = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)
