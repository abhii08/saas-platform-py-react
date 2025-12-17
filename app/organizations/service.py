from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.organizations.models import Organization
from app.organizations.schemas import OrganizationCreate, OrganizationUpdate
from typing import List, Optional


class OrganizationService:
    """
    Service layer for organization operations.
    Handles CRUD operations for organizations.
    """
    
    @staticmethod
    def create_organization(db: Session, data: OrganizationCreate) -> Organization:
        """
        Create a new organization.
        
        Args:
            db: Database session
            data: Organization creation data
            
        Returns:
            Created organization
            
        Raises:
            HTTPException: If slug already exists
        """
        existing = db.query(Organization).filter(Organization.slug == data.slug).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization slug already exists"
            )
        
        organization = Organization(**data.model_dump())
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization
    
    @staticmethod
    def get_organization(db: Session, organization_id: int) -> Organization:
        """
        Get organization by ID.
        
        Args:
            db: Database session
            organization_id: Organization ID
            
        Returns:
            Organization instance
            
        Raises:
            HTTPException: If organization not found
        """
        organization = db.query(Organization).filter(Organization.id == organization_id).first()
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        return organization
    
    @staticmethod
    def list_organizations(db: Session, skip: int = 0, limit: int = 20) -> List[Organization]:
        """
        List all organizations with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of organizations
        """
        return db.query(Organization).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_organization(db: Session, organization_id: int, data: OrganizationUpdate) -> Organization:
        """
        Update organization.
        
        Args:
            db: Database session
            organization_id: Organization ID
            data: Update data
            
        Returns:
            Updated organization
            
        Raises:
            HTTPException: If organization not found or slug conflict
        """
        organization = OrganizationService.get_organization(db, organization_id)
        
        update_data = data.model_dump(exclude_unset=True)
        
        if "slug" in update_data:
            existing = db.query(Organization).filter(
                Organization.slug == update_data["slug"],
                Organization.id != organization_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization slug already exists"
                )
        
        for field, value in update_data.items():
            setattr(organization, field, value)
        
        db.commit()
        db.refresh(organization)
        return organization
    
    @staticmethod
    def delete_organization(db: Session, organization_id: int) -> None:
        """
        Delete organization (soft delete by setting is_active=False).
        
        Args:
            db: Database session
            organization_id: Organization ID
            
        Raises:
            HTTPException: If organization not found
        """
        organization = OrganizationService.get_organization(db, organization_id)
        organization.is_active = False
        db.commit()
