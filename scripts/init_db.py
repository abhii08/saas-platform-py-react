import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.roles.models import Role
from app.organizations.models import Organization
from app.users.models import User, UserOrganization
from app.projects.models import Project
from app.boards.models import Board
from app.tasks.models import Task
from app.comments.models import Comment


def init_roles(db: Session):
    """
    Initialize default roles in the database.
    """
    roles = [
        {"name": "ORG_ADMIN", "description": "Organization Administrator - Full access to organization resources"},
        {"name": "PROJECT_MANAGER", "description": "Project Manager - Manage projects and teams"},
        {"name": "MEMBER", "description": "Member - View and contribute to assigned tasks"}
    ]
    
    for role_data in roles:
        existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
            print(f"Created role: {role_data['name']}")
        else:
            print(f"Role already exists: {role_data['name']}")
    
    db.commit()


def init_database():
    """
    Initialize the database with tables and default data.
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    db = SessionLocal()
    try:
        print("\nInitializing default roles...")
        init_roles(db)
        print("\nDatabase initialization completed successfully!")
    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
