from sqlalchemy.orm import Session
from app.users.models import User, UserOrganization
from typing import List, Tuple


class UserService:
    """
    Service layer for user operations.
    """
    
    @staticmethod
    def list_users_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100) -> Tuple[List[User], int]:
        """
        List all users in a specific organization.
        
        Args:
            db: Database session
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (users list, total count)
        """
        query = db.query(User).join(
            UserOrganization, User.id == UserOrganization.user_id
        ).filter(
            UserOrganization.organization_id == organization_id,
            UserOrganization.is_active == True,
            User.is_active == True
        )
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        return users, total
