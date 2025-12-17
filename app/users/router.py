from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.core.dependencies import get_current_user, get_tenant_id
from app.users.schemas import UserResponse
from app.users.service import UserService
from app.utils.pagination import PaginatedResponse, PaginationParams


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = 1,
    page_size: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List all users in the current organization.
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    users, total = UserService.list_users_by_organization(db, tenant_id, pagination.skip, pagination.limit)
    
    return PaginatedResponse.create(
        items=users,
        total=total,
        page=page,
        page_size=page_size
    )
