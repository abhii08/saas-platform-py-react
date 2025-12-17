from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    """Base schema for comment data."""
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    """Schema for creating a new comment."""
    task_id: int


class CommentUpdate(BaseModel):
    """Schema for updating a comment."""
    content: Optional[str] = Field(None, min_length=1)


class CommentResponse(CommentBase):
    """Schema for comment response."""
    id: int
    task_id: int
    user_id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
