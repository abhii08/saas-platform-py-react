from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.organizations.schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.organizations.service import OrganizationService


router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new organization.
    
    Note: In production, you may want to restrict this to super admins only.
    """
    organization = OrganizationService.create_organization(db, data)
    return organization


@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List all organizations.
    
    Note: In production, users should only see organizations they belong to.
    """
    organizations = OrganizationService.list_organizations(db, skip, limit)
    return organizations


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get organization by ID.
    """
    organization = OrganizationService.get_organization(db, organization_id)
    return organization


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: int,
    data: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Update organization.
    
    Requires ORG_ADMIN role.
    """
    organization = OrganizationService.update_organization(db, organization_id, data)
    return organization


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Delete (deactivate) organization.
    
    Requires ORG_ADMIN role.
    """
    OrganizationService.delete_organization(db, organization_id)
