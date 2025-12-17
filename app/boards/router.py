from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.core.dependencies import get_current_user, get_tenant_id, require_manager_or_admin
from app.boards.schemas import BoardCreate, BoardUpdate, BoardResponse
from app.boards.service import BoardService


router = APIRouter(prefix="/boards", tags=["Boards"])


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    data: BoardCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_manager_or_admin),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Create a new board within a project.
    
    Requires PROJECT_MANAGER or ORG_ADMIN role.
    """
    board = BoardService.create_board(db, data, tenant_id)
    return board


@router.get("/project/{project_id}", response_model=List[BoardResponse])
async def list_boards_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List all boards for a specific project.
    """
    boards = BoardService.list_boards_by_project(db, project_id, tenant_id)
    return boards


@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Get board by ID.
    """
    board = BoardService.get_board(db, board_id, tenant_id)
    return board


@router.put("/{board_id}", response_model=BoardResponse)
async def update_board(
    board_id: int,
    data: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_manager_or_admin),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Update board.
    
    Requires PROJECT_MANAGER or ORG_ADMIN role.
    """
    board = BoardService.update_board(db, board_id, data, tenant_id)
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_manager_or_admin),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Delete (deactivate) board.
    
    Requires PROJECT_MANAGER or ORG_ADMIN role.
    """
    BoardService.delete_board(db, board_id, tenant_id)
