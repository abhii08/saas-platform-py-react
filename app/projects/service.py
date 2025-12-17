from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.projects.models import Project
from app.projects.schemas import ProjectCreate, ProjectUpdate
from typing import List


class ProjectService:
    """
    Service layer for project operations.
    Enforces tenant isolation for all operations.
    """
    
    @staticmethod
    def create_project(db: Session, data: ProjectCreate, organization_id: int, user_id: int) -> Project:
        """
        Create a new project within the current tenant.
        
        Args:
            db: Database session
            data: Project creation data
            organization_id: Current tenant ID
            user_id: ID of user creating the project
            
        Returns:
            Created project
            
        Raises:
            HTTPException: If slug already exists within organization
        """
        existing = db.query(Project).filter(
            Project.organization_id == organization_id,
            Project.slug == data.slug
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project slug already exists in this organization"
            )
        
        project = Project(
            **data.model_dump(),
            organization_id=organization_id,
            created_by=user_id
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    @staticmethod
    def get_project(db: Session, project_id: int, organization_id: int) -> Project:
        """
        Get project by ID with tenant isolation.
        
        Args:
            db: Database session
            project_id: Project ID
            organization_id: Current tenant ID
            
        Returns:
            Project instance
            
        Raises:
            HTTPException: If project not found or belongs to different tenant
        """
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.organization_id == organization_id
        ).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return project
    
    @staticmethod
    def list_projects(db: Session, organization_id: int, skip: int = 0, limit: int = 20) -> tuple[List[Project], int]:
        """
        List projects for current tenant with pagination.
        
        Args:
            db: Database session
            organization_id: Current tenant ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (projects list, total count)
        """
        query = db.query(Project).filter(
            Project.organization_id == organization_id,
            Project.is_active == True
        )
        total = query.count()
        projects = query.offset(skip).limit(limit).all()
        return projects, total
    
    @staticmethod
    def update_project(db: Session, project_id: int, data: ProjectUpdate, organization_id: int) -> Project:
        """
        Update project with tenant isolation.
        
        Args:
            db: Database session
            project_id: Project ID
            data: Update data
            organization_id: Current tenant ID
            
        Returns:
            Updated project
            
        Raises:
            HTTPException: If project not found or slug conflict
        """
        project = ProjectService.get_project(db, project_id, organization_id)
        
        update_data = data.model_dump(exclude_unset=True)
        
        if "slug" in update_data:
            existing = db.query(Project).filter(
                Project.organization_id == organization_id,
                Project.slug == update_data["slug"],
                Project.id != project_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Project slug already exists in this organization"
                )
        
        for field, value in update_data.items():
            setattr(project, field, value)
        
        db.commit()
        db.refresh(project)
        return project
    
    @staticmethod
    def delete_project(db: Session, project_id: int, organization_id: int) -> None:
        """
        Delete project (soft delete) with tenant isolation.
        
        Args:
            db: Database session
            project_id: Project ID
            organization_id: Current tenant ID
            
        Raises:
            HTTPException: If project not found
        """
        project = ProjectService.get_project(db, project_id, organization_id)
        project.is_active = False
        db.commit()
