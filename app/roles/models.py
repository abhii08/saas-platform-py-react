from sqlalchemy import Column, Integer, String, Text
from app.database.base import Base, TimestampMixin


class Role(Base, TimestampMixin):
    """
    Role model - defines available roles in the system.
    
    Standard roles:
    - ORG_ADMIN: Full access to organization resources
    - PROJECT_MANAGER: Manage projects and teams
    - MEMBER: View and contribute to assigned tasks
    
    Roles are assigned per organization via user_organizations table.
    """
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
