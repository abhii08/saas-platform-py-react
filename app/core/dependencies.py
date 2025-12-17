from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import decode_token, verify_token_type
from app.database.session import get_db


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Extract and validate current user from JWT token.
    
    This dependency:
    1. Extracts the JWT token from Authorization header
    2. Validates the token signature and expiration
    3. Verifies it's an access token (not refresh)
    4. Returns user information including tenant context
    
    Args:
        credentials: HTTP Bearer token from request header
        db: Database session
        
    Returns:
        Dictionary containing user_id, email, organization_id, role
        
    Raises:
        HTTPException: If token is invalid, expired, or user not found
    """
    token = credentials.credentials
    payload = decode_token(token)
    verify_token_type(payload, "access")
    
    user_id: Optional[int] = payload.get("user_id")
    email: Optional[str] = payload.get("email")
    organization_id: Optional[int] = payload.get("organization_id")
    role: Optional[str] = payload.get("role")
    
    if user_id is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": user_id,
        "email": email,
        "organization_id": organization_id,
        "role": role
    }


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Ensure the current user is active.
    Can be extended to check user.is_active from database.
    
    Args:
        current_user: User info from get_current_user dependency
        
    Returns:
        User information dictionary
    """
    return current_user


async def get_tenant_id(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> int:
    """
    Extract tenant (organization) ID from current user context.
    
    This is critical for multi-tenant isolation - every query must be scoped
    to the current tenant to prevent cross-tenant data access.
    
    Args:
        current_user: User info from get_current_user dependency
        
    Returns:
        Organization ID (tenant_id)
        
    Raises:
        HTTPException: If user is not associated with an organization
    """
    organization_id = current_user.get("organization_id")
    
    if organization_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not associated with any organization"
        )
    
    return organization_id


async def require_role(required_roles: list[str]):
    """
    Factory function to create role-based authorization dependencies.
    
    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(user = Depends(require_role(["ORG_ADMIN"]))):
            ...
    
    Args:
        required_roles: List of allowed role names
        
    Returns:
        Dependency function that validates user role
    """
    async def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_role = current_user.get("role")
        
        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(required_roles)}"
            )
        
        return current_user
    
    return role_checker


async def require_admin(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Require ORG_ADMIN role for the current user.
    
    Args:
        current_user: User info from get_current_user dependency
        
    Returns:
        User information dictionary
        
    Raises:
        HTTPException: If user is not an ORG_ADMIN
    """
    if current_user.get("role") != "ORG_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user


async def require_manager_or_admin(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Require PROJECT_MANAGER or ORG_ADMIN role.
    
    Args:
        current_user: User info from get_current_user dependency
        
    Returns:
        User information dictionary
        
    Raises:
        HTTPException: If user doesn't have required role
    """
    user_role = current_user.get("role")
    
    if user_role not in ["ORG_ADMIN", "PROJECT_MANAGER"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or Admin privileges required"
        )
    
    return current_user
