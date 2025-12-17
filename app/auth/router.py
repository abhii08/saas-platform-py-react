from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.schemas import (
    LoginRequest, LoginResponse,
    RegisterRequest, RegisterResponse,
    RefreshTokenRequest, RefreshTokenResponse
)
from app.auth.service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user and create their organization.
    
    This endpoint:
    1. Creates a new user account
    2. Creates a new organization
    3. Assigns the user as ORG_ADMIN
    4. Returns JWT tokens for immediate login
    """
    result = AuthService.register_user(db, data)
    return RegisterResponse(**result, token_type="bearer")


@router.post("/login", response_model=LoginResponse)
async def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens.
    
    Returns both access token (short-lived) and refresh token (long-lived).
    """
    result = AuthService.login_user(db, data)
    return LoginResponse(**result, token_type="bearer")


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Generate new access token using refresh token.
    
    Use this endpoint when the access token expires to get a new one
    without requiring the user to login again.
    """
    access_token = AuthService.refresh_access_token(db, data.refresh_token)
    return RefreshTokenResponse(access_token=access_token, token_type="bearer")
