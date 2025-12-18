from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.tasks.models import Task
from app.boards.models import Board
from app.tasks.schemas import TaskCreate, TaskUpdate
from typing import List, Optional


class TaskService:
    """
    Service layer for task operations.
    Enforces tenant isolation through board -> project relationship.
    """
    
    @staticmethod
    def create_task(db: Session, data: TaskCreate, organization_id: int, user_id: int) -> Task:
        """
        Create a new task within a board.
        
        Validates that the board belongs to the current tenant.
        
        Args:
            db: Database session
            data: Task creation data
            organization_id: Current tenant ID
            user_id: ID of user creating the task
            
        Returns:
            Created task
            
        Raises:
            HTTPException: If board not found or belongs to different tenant
        """
        board = db.query(Board).filter(
            Board.id == data.board_id,
            Board.organization_id == organization_id
        ).first()
        
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found"
            )
        
        task = Task(
            **data.model_dump(),
            organization_id=organization_id,
            created_by=user_id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def get_task(db: Session, task_id: int, organization_id: int) -> Task:
        """
        Get task by ID with tenant isolation.
        
        Args:
            db: Database session
            task_id: Task ID
            organization_id: Current tenant ID
            
        Returns:
            Task instance
            
        Raises:
            HTTPException: If task not found or belongs to different tenant
        """
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.organization_id == organization_id
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    
    @staticmethod
    def list_tasks_by_board(
        db: Session,
        board_id: int,
        organization_id: int,
        status: Optional[str] = None,
        assigned_to: Optional[int] = None
    ) -> List[Task]:
        """
        List tasks for a specific board with optional filters.
        
        Args:
            db: Database session
            board_id: Board ID
            organization_id: Current tenant ID
            status: Optional status filter
            assigned_to: Optional assignee filter
            
        Returns:
            List of tasks
        """
        query = db.query(Task).filter(
            Task.board_id == board_id,
            Task.organization_id == organization_id
        )
        
        if status:
            query = query.filter(Task.status == status)
        
        if assigned_to:
            query = query.filter(Task.assigned_to == assigned_to)
        
        return query.order_by(Task.position, Task.created_at).all()
    
    @staticmethod
    def update_task(db: Session, task_id: int, data: TaskUpdate, organization_id: int, user_id: int = None, user_role: str = None) -> Task:
        """
        Update task with tenant isolation and ownership validation.
        
        RBAC Rules:
        - ORG_ADMIN: Can update any task
        - PROJECT_MANAGER: Can update any task
        - MEMBER: Can only update tasks they created or are assigned to
        
        Args:
            db: Database session
            task_id: Task ID
            data: Update data
            organization_id: Current tenant ID
            user_id: ID of user making the update (for MEMBER validation)
            user_role: Role of user making the update
            
        Returns:
            Updated task
            
        Raises:
            HTTPException: If MEMBER tries to update someone else's task
        """
        task = TaskService.get_task(db, task_id, organization_id)
        
        # MEMBER role can only update their own tasks (created by them or assigned to them)
        if user_role == "MEMBER" and user_id:
            if task.created_by != user_id and task.assigned_to != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Members can only update tasks they created or are assigned to"
                )
        
        update_data = data.model_dump(exclude_unset=True)
        
        # If board_id is being updated, validate the new board belongs to same organization
        if 'board_id' in update_data and update_data['board_id'] is not None:
            board = db.query(Board).filter(
                Board.id == update_data['board_id'],
                Board.organization_id == organization_id
            ).first()
            
            if not board:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Board not found"
                )
        
        for field, value in update_data.items():
            setattr(task, field, value)
        
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def delete_task(db: Session, task_id: int, organization_id: int, user_id: int = None, user_role: str = None) -> None:
        """
        Delete task (hard delete) with tenant isolation and role validation.
        
        RBAC Rules:
        - ORG_ADMIN: Can delete any task
        - PROJECT_MANAGER: Can delete any task
        - MEMBER: NOT ALLOWED to delete tasks
        
        Args:
            db: Database session
            task_id: Task ID
            organization_id: Current tenant ID
            user_id: ID of user making the deletion
            user_role: Role of user making the deletion
            
        Raises:
            HTTPException: If MEMBER tries to delete any task
        """
        task = TaskService.get_task(db, task_id, organization_id)
        
        # MEMBER role is NOT allowed to delete any tasks
        if user_role == "MEMBER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Members are not allowed to delete tasks"
            )
        
        db.delete(task)
        db.commit()
