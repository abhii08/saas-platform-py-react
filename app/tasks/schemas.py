from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.tasks.models import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base schema for task data."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    position: int = Field(default=0, ge=0)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    board_id: int


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    board_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    position: Optional[int] = Field(None, ge=0)


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    board_id: int
    organization_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
