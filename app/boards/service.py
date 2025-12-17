from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.boards.models import Board
from app.projects.models import Project
from app.boards.schemas import BoardCreate, BoardUpdate
from typing import List


class BoardService:
    """
    Service layer for board operations.
    Enforces tenant isolation through project relationship.
    """
    
    @staticmethod
    def create_board(db: Session, data: BoardCreate, organization_id: int) -> Board:
        """
        Create a new board within a project.
        
        Validates that the project belongs to the current tenant.
        
        Args:
            db: Database session
            data: Board creation data
            organization_id: Current tenant ID
            
        Returns:
            Created board
            
        Raises:
            HTTPException: If project not found or belongs to different tenant
        """
        project = db.query(Project).filter(
            Project.id == data.project_id,
            Project.organization_id == organization_id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        board = Board(
            **data.model_dump(),
            organization_id=organization_id
        )
        db.add(board)
        db.commit()
        db.refresh(board)
        return board
    
    @staticmethod
    def get_board(db: Session, board_id: int, organization_id: int) -> Board:
        """
        Get board by ID with tenant isolation.
        
        Args:
            db: Database session
            board_id: Board ID
            organization_id: Current tenant ID
            
        Returns:
            Board instance
            
        Raises:
            HTTPException: If board not found or belongs to different tenant
        """
        board = db.query(Board).filter(
            Board.id == board_id,
            Board.organization_id == organization_id
        ).first()
        
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found"
            )
        return board
    
    @staticmethod
    def list_boards_by_project(db: Session, project_id: int, organization_id: int) -> List[Board]:
        """
        List all boards for a specific project.
        
        Args:
            db: Database session
            project_id: Project ID
            organization_id: Current tenant ID
            
        Returns:
            List of boards
        """
        return db.query(Board).filter(
            Board.project_id == project_id,
            Board.organization_id == organization_id
        ).order_by(Board.position).all()
    
    @staticmethod
    def update_board(db: Session, board_id: int, data: BoardUpdate, organization_id: int) -> Board:
        """
        Update board with tenant isolation.
        
        Args:
            db: Database session
            board_id: Board ID
            data: Update data
            organization_id: Current tenant ID
            
        Returns:
            Updated board
        """
        board = BoardService.get_board(db, board_id, organization_id)
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(board, field, value)
        
        db.commit()
        db.refresh(board)
        return board
    
    @staticmethod
    def delete_board(db: Session, board_id: int, organization_id: int) -> None:
        """
        Delete board (soft delete) with tenant isolation.
        
        Args:
            db: Database session
            board_id: Board ID
            organization_id: Current tenant ID
        """
        board = BoardService.get_board(db, board_id, organization_id)
        board.is_active = False
        db.commit()
