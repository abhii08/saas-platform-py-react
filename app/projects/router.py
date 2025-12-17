from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.dependencies import get_current_user, get_tenant_id, require_manager_or_admin
from app.projects.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.projects.service import ProjectService
from app.utils.pagination import PaginatedResponse, PaginationParams


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_manager_or_admin),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Create a new project.
    
    Requires PROJECT_MANAGER or ORG_ADMIN role.
    Project is automatically scoped to the current tenant.
    """
    project = ProjectService.create_project(db, data, tenant_id, current_user["user_id"])
    return project


@router.get("/", response_model=PaginatedResponse[ProjectResponse])
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List all projects for the current organization.
    
    Results are automatically filtered by tenant_id.
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    projects, total = ProjectService.list_projects(db, tenant_id, pagination.skip, pagination.limit)
    
    return PaginatedResponse.create(
        items=projects,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Get project by ID.
    
    Tenant isolation ensures users can only access projects in their organization.
    """
    project = ProjectService.get_project(db, project_id, tenant_id)
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_manager_or_admin),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Update project.
    
    Requires PROJECT_MANAGER or ORG_ADMIN role.
    """
    project = ProjectService.update_project(db, project_id, data, tenant_id)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_manager_or_admin),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Delete (deactivate) project.
    
    Requires PROJECT_MANAGER or ORG_ADMIN role.
    """
    ProjectService.delete_project(db, project_id, tenant_id)
