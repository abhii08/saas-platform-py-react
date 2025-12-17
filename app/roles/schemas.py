from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RoleBase(BaseModel):
    """Base schema for role data."""
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a new role."""
    pass


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None


class RoleResponse(RoleBase):
    """Schema for role response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
