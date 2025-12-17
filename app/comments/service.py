from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.comments.models import Comment
from app.tasks.models import Task
from app.comments.schemas import CommentCreate, CommentUpdate
from typing import List


class CommentService:
    """
    Service layer for comment operations.
    Enforces tenant isolation through task -> board -> project relationship.
    """
    
    @staticmethod
    def create_comment(db: Session, data: CommentCreate, organization_id: int, user_id: int) -> Comment:
        """
        Create a new comment on a task.
        
        Validates that the task belongs to the current tenant.
        
        Args:
            db: Database session
            data: Comment creation data
            organization_id: Current tenant ID
            user_id: ID of user creating the comment
            
        Returns:
            Created comment
            
        Raises:
            HTTPException: If task not found or belongs to different tenant
        """
        task = db.query(Task).filter(
            Task.id == data.task_id,
            Task.organization_id == organization_id
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        comment = Comment(
            task_id=data.task_id,
            content=data.content,
            organization_id=organization_id,
            user_id=user_id
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    
    @staticmethod
    def get_comment(db: Session, comment_id: int, organization_id: int) -> Comment:
        """
        Get comment by ID with tenant isolation.
        
        Args:
            db: Database session
            comment_id: Comment ID
            organization_id: Current tenant ID
            
        Returns:
            Comment instance
            
        Raises:
            HTTPException: If comment not found or belongs to different tenant
        """
        comment = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.organization_id == organization_id
        ).first()
        
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        return comment
    
    @staticmethod
    def list_comments_by_task(db: Session, task_id: int, organization_id: int) -> List[Comment]:
        """
        List all comments for a specific task.
        
        Args:
            db: Database session
            task_id: Task ID
            organization_id: Current tenant ID
            
        Returns:
            List of comments ordered by creation time
        """
        return db.query(Comment).filter(
            Comment.task_id == task_id,
            Comment.organization_id == organization_id
        ).order_by(Comment.created_at).all()
    
    @staticmethod
    def update_comment(db: Session, comment_id: int, data: CommentUpdate, organization_id: int, user_id: int) -> Comment:
        """
        Update comment with tenant isolation and ownership check.
        
        Args:
            db: Database session
            comment_id: Comment ID
            data: Update data
            organization_id: Current tenant ID
            user_id: ID of user attempting update
            
        Returns:
            Updated comment
            
        Raises:
            HTTPException: If user doesn't own the comment
        """
        comment = CommentService.get_comment(db, comment_id, organization_id)
        
        if comment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own comments"
            )
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(comment, field, value)
        
        db.commit()
        db.refresh(comment)
        return comment
    
    @staticmethod
    def delete_comment(db: Session, comment_id: int, organization_id: int, user_id: int) -> None:
        """
        Delete comment with tenant isolation and ownership check.
        
        Args:
            db: Database session
            comment_id: Comment ID
            organization_id: Current tenant ID
            user_id: ID of user attempting deletion
            
        Raises:
            HTTPException: If user doesn't own the comment
        """
        comment = CommentService.get_comment(db, comment_id, organization_id)
        
        if comment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own comments"
            )
        
        db.delete(comment)
        db.commit()
