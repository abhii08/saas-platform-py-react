from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.users.models import User, UserOrganization
from app.organizations.models import Organization
from app.roles.models import Role
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token, verify_token_type
from app.auth.schemas import LoginRequest, RegisterRequest
from typing import Dict, Any


class AuthService:
    """
    Service layer for authentication operations.
    Handles user registration, login, and token management.
    """
    
    @staticmethod
    def register_user(db: Session, data: RegisterRequest) -> Dict[str, Any]:
        """
        Register a new user and join an existing organization.
        
        This is a multi-step transaction:
        1. Check if email already exists
        2. Verify organization exists and is active
        3. Create new user
        4. Assign selected role to user in the organization
        5. Generate JWT tokens
        
        Args:
            db: Database session
            data: Registration data
            
        Returns:
            Dictionary with user_id, organization_id, and tokens
            
        Raises:
            HTTPException: If email already exists or organization not found
        """
        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        organization = db.query(Organization).filter(
            Organization.id == data.organization_id,
            Organization.is_active == True
        ).first()
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization not found or inactive"
            )
        
        user = User(
            email=data.email,
            password_hash=get_password_hash(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=True,
            is_verified=False
        )
        db.add(user)
        db.flush()
        
        selected_role = db.query(Role).filter(Role.name == data.role).first()
        if not selected_role:
            selected_role = Role(name=data.role, description=f"{data.role.replace('_', ' ').title()}")
            db.add(selected_role)
            db.flush()
        
        user_org = UserOrganization(
            user_id=user.id,
            organization_id=organization.id,
            role_id=selected_role.id,
            is_active=True
        )
        db.add(user_org)
        db.commit()
        
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": organization.id,
            "role": data.role
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"user_id": user.id})
        
        return {
            "user_id": user.id,
            "organization_id": organization.id,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def login_user(db: Session, data: LoginRequest, organization_id: int = None) -> Dict[str, str]:
        """
        Authenticate user and generate tokens.
        
        Args:
            db: Database session
            data: Login credentials
            organization_id: Optional specific organization to login to
            
        Returns:
            Dictionary with access_token and refresh_token
            
        Raises:
            HTTPException: If credentials are invalid or user not found
        """
        user = db.query(User).filter(User.email == data.email).first()
        
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        user_org_query = db.query(UserOrganization, Role).join(
            Role, UserOrganization.role_id == Role.id
        ).filter(
            UserOrganization.user_id == user.id,
            UserOrganization.is_active == True
        )
        
        if organization_id:
            user_org_query = user_org_query.filter(UserOrganization.organization_id == organization_id)
        
        user_org_data = user_org_query.first()
        
        if not user_org_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not associated with any active organization"
            )
        
        user_org, role = user_org_data
        
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": user_org.organization_id,
            "role": role.name
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"user_id": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> str:
        """
        Generate new access token from refresh token.
        
        Args:
            db: Database session
            refresh_token: Valid refresh token
            
        Returns:
            New access token
            
        Raises:
            HTTPException: If refresh token is invalid
        """
        payload = decode_token(refresh_token)
        verify_token_type(payload, "refresh")
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        user_org_data = db.query(UserOrganization, Role).join(
            Role, UserOrganization.role_id == Role.id
        ).filter(
            UserOrganization.user_id == user.id,
            UserOrganization.is_active == True
        ).first()
        
        if not user_org_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not associated with any active organization"
            )
        
        user_org, role = user_org_data
        
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": user_org.organization_id,
            "role": role.name
        }
        
        return create_access_token(token_data)
