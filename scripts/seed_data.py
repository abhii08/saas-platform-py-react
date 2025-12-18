import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.organizations.models import Organization
from app.users.models import User, UserOrganization
from app.roles.models import Role
from app.projects.models import Project
from app.boards.models import Board
from app.tasks.models import Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash


def seed_data():
    """
    Seed the database with sample data for testing.
    """
    db = SessionLocal()
    
    try:
        print("Seeding database with sample data...")
        
        admin_role = db.query(Role).filter(Role.name == "ORG_ADMIN").first()
        manager_role = db.query(Role).filter(Role.name == "PROJECT_MANAGER").first()
        member_role = db.query(Role).filter(Role.name == "MEMBER").first()
        
        org1 = Organization(name="Fxis.ai Corporation", slug="fxis-corp", is_active=True)
        org2 = Organization(name="Tech Startup Inc", slug="tech-startup", is_active=True)
        db.add_all([org1, org2])
        db.flush()
        
        user1 = User(
            email="admin@fxis.ai",
            password_hash=get_password_hash("admin123"),
            first_name="Hemen",
            last_name="Admin",
            is_active=True,
            is_verified=True
        )
        user2 = User(
            email="manager@fxis.ai",
            password_hash=get_password_hash("manager123"),
            first_name="Husain",
            last_name="Manager",
            is_active=True,
            is_verified=True
        )
        user3 = User(
            email="member@fxis.ai",
            password_hash=get_password_hash("member123"),
            first_name="Abhinav",
            last_name="Member",
            is_active=True,
            is_verified=True
        )
        db.add_all([user1, user2, user3])
        db.flush()
        
        user_org1 = UserOrganization(user_id=user1.id, organization_id=org1.id, role_id=admin_role.id, is_active=True)
        user_org2 = UserOrganization(user_id=user2.id, organization_id=org1.id, role_id=manager_role.id, is_active=True)
        user_org3 = UserOrganization(user_id=user3.id, organization_id=org1.id, role_id=member_role.id, is_active=True)
        db.add_all([user_org1, user_org2, user_org3])
        db.flush()
        
        project1 = Project(
            name="Website Redesign",
            description="Redesign company website with modern UI",
            slug="website-redesign",
            organization_id=org1.id,
            created_by=user1.id,
            is_active=True
        )
        project2 = Project(
            name="Mobile App Development",
            description="Build iOS and Android mobile applications",
            slug="mobile-app",
            organization_id=org1.id,
            created_by=user2.id,
            is_active=True
        )
        db.add_all([project1, project2])
        db.flush()
        
        board1 = Board(
            name="Sprint 1",
            description="First sprint tasks",
            project_id=project1.id,
            organization_id=org1.id,
            position=0,
            is_active=True
        )
        board2 = Board(
            name="Backlog",
            description="Future tasks",
            project_id=project1.id,
            organization_id=org1.id,
            position=1,
            is_active=True
        )
        db.add_all([board1, board2])
        db.flush()
        
        task1 = Task(
            title="Design homepage mockup",
            description="Create high-fidelity mockup for new homepage",
            board_id=board1.id,
            organization_id=org1.id,
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            assigned_to=user2.id,
            created_by=user1.id,
            position=0
        )
        task2 = Task(
            title="Setup development environment",
            description="Configure local dev environment for the project",
            board_id=board1.id,
            organization_id=org1.id,
            status=TaskStatus.DONE,
            priority=TaskPriority.MEDIUM,
            assigned_to=user3.id,
            created_by=user2.id,
            position=1
        )
        task3 = Task(
            title="Write API documentation",
            description="Document all API endpoints",
            board_id=board2.id,
            organization_id=org1.id,
            status=TaskStatus.TODO,
            priority=TaskPriority.LOW,
            assigned_to=user3.id,
            created_by=user1.id,
            position=0
        )
        db.add_all([task1, task2, task3])
        
        db.commit()
        print("Database seeded successfully!")
        print("\nSample credentials:")
        print("  Admin: admin@fxis.ai / admin123")
        print("  Manager: manager@fxis.ai / manager123")
        print("  Member: member@fxis.ai / member123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
