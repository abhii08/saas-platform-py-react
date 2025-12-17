from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BoardBase(BaseModel):
    """Base schema for board data."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    position: int = Field(default=0, ge=0)


class BoardCreate(BoardBase):
    """Schema for creating a new board."""
    project_id: int


class BoardUpdate(BaseModel):
    """Schema for updating a board."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    position: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class BoardResponse(BoardBase):
    """Schema for board response."""
    id: int
    project_id: int
    organization_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
