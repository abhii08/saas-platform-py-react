from sqlalchemy import Column, Integer, Text, ForeignKey
from app.database.base import Base, TimestampMixin, TenantMixin


class Comment(Base, TimestampMixin, TenantMixin):
    """
    Comment model - represents a comment on a task.
    
    Multi-tenant isolation:
    - Includes organization_id (via TenantMixin)
    - Belongs to task -> board -> project -> organization
    - Ensures comments are only visible within tenant context
    """
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
