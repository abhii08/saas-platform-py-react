from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.core.dependencies import get_current_user, get_tenant_id
from app.comments.schemas import CommentCreate, CommentUpdate, CommentResponse
from app.comments.service import CommentService


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Create a new comment on a task.
    
    All members can create comments.
    """
    comment = CommentService.create_comment(db, data, tenant_id, current_user["user_id"])
    return comment


@router.get("/task/{task_id}", response_model=List[CommentResponse])
async def list_comments_by_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List all comments for a specific task.
    """
    comments = CommentService.list_comments_by_task(db, task_id, tenant_id)
    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Get comment by ID.
    """
    comment = CommentService.get_comment(db, comment_id, tenant_id)
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Update comment.
    
    Users can only update their own comments.
    """
    comment = CommentService.update_comment(db, comment_id, data, tenant_id, current_user["user_id"])
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Delete comment.
    
    Users can only delete their own comments.
    """
    CommentService.delete_comment(db, comment_id, tenant_id, current_user["user_id"])
