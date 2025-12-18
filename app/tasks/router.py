from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.core.dependencies import get_current_user, get_tenant_id
from app.tasks.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.tasks.service import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Create a new task within a board.
    
    All members can create tasks.
    """
    task = TaskService.create_task(db, data, tenant_id, current_user["user_id"])
    return task


@router.get("/board/{board_id}", response_model=List[TaskResponse])
async def list_tasks_by_board(
    board_id: int,
    status: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List all tasks for a specific board.
    
    Optional filters:
    - status: Filter by task status
    - assigned_to: Filter by assignee user ID
    """
    tasks = TaskService.list_tasks_by_board(db, board_id, tenant_id, status, assigned_to)
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Get task by ID.
    """
    task = TaskService.get_task(db, task_id, tenant_id)
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Update task.
    
    RBAC Rules:
    - ORG_ADMIN and PROJECT_MANAGER: Can update any task
    - MEMBER: Can only update tasks they created or are assigned to
    """
    task = TaskService.update_task(
        db, 
        task_id, 
        data, 
        tenant_id, 
        user_id=current_user["user_id"],
        user_role=current_user.get("role")
    )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Delete task.
    
    RBAC Rules:
    - ORG_ADMIN: Can delete any task
    - PROJECT_MANAGER: Can delete any task
    - MEMBER: NOT ALLOWED to delete tasks
    """
    TaskService.delete_task(
        db, 
        task_id, 
        tenant_id,
        user_id=current_user["user_id"],
        user_role=current_user.get("role")
    )
