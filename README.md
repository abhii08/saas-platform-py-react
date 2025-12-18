# Multi-Tenant SaaS Project Management Platform

A production-ready, multi-tenant SaaS platform built with FastAPI, React, and PostgreSQL.

## Features

- 🏢 **Multi-Tenancy**: Shared schema with strict tenant isolation
- 🔐 **Authentication**: JWT-based auth with access & refresh tokens
- 👥 **RBAC**: Role-based access control (ORG_ADMIN, PROJECT_MANAGER, MEMBER)
- 📊 **Project Management**: Projects, Boards, Tasks, Comments
- 🚀 **Production-Ready**: Docker, PostgreSQL support
- 📚 **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- PostgreSQL

**Frontend:**
- React 18.2
- Vite (Build tool)
- React Router v6
- TailwindCSS (Styling)
- Radix UI (Components)
- Lucide React (Icons)
- Axios (HTTP client)
- JWT Authentication
- Role-based UI

## Architecture

```
React → FastAPI → Services → SQLAlchemy → PostgreSQL
```

## Quick Start with Docker (Recommended)

1. **Start the services:**
```bash
docker-compose up
```

2. **Initialize the database:**
```bash
docker exec -it saas_backend python scripts/init_db.py
```

3. **Seed sample data (optional):**
```bash
docker exec -it saas_backend python scripts/seed_data.py
```

4. **Access the application:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

### Sample Credentials (after seeding)
```
Admin:    admin@fxis.ai / admin123
Manager:  manager@fxis.ai / manager123
Member:   member@fxis.ai / member123
```

## Manual Setup (Without Docker)

### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```bash
creatdb saas_db
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python scripts/init_db.py
```

6. Seed sample data (optional):
```bash
python scripts/seed_data.py
```

7. Start the server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

API will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs
Frontend: http://localhost:5173

## Project Structure

```
app/
├── main.py                 # Application entry point
├── core/                   # Core configuration
│   ├── config.py          # Settings management
│   ├── security.py        # JWT & password utilities
│   └── dependencies.py    # Shared dependencies
├── auth/                   # Authentication module
├── organizations/          # Organization management
├── users/                  # User management
├── projects/              # Project management
├── boards/                # Board management
├── tasks/                 # Task management
├── comments/              # Comment management
├── roles/                 # Role management
└── database/              # Database configuration
    ├── session.py         # DB session management
    └── base.py           # Base model classes
```

## Multi-Tenancy

Every database query is automatically scoped to the current tenant (organization). The `tenant_id` is extracted from the JWT token and injected into all queries.

## RBAC Roles

- **ORG_ADMIN**: Full access to organization resources
- **PROJECT_MANAGER**: Manage projects and teams
- **MEMBER**: View and contribute to assigned tasks

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user and create organization
- `POST /api/v1/auth/login` - Login and get JWT tokens
- `POST /api/v1/auth/refresh` - Refresh access token

### Organizations
- `GET /api/v1/organizations` - List organizations
- `POST /api/v1/organizations` - Create organization
- `GET /api/v1/organizations/{id}` - Get organization details
- `PUT /api/v1/organizations/{id}` - Update organization (ORG_ADMIN)
- `DELETE /api/v1/organizations/{id}` - Delete organization (ORG_ADMIN)

### Users
- `GET /api/v1/users` - List users in current organization

### Projects
- `GET /api/v1/projects` - List projects (paginated)
- `POST /api/v1/projects` - Create project (MANAGER/ADMIN)
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project (MANAGER/ADMIN)
- `DELETE /api/v1/projects/{id}` - Soft delete project (MANAGER/ADMIN)

### Boards
- `GET /api/v1/boards/project/{project_id}` - List boards by project
- `POST /api/v1/boards` - Create board (MANAGER/ADMIN)
- `GET /api/v1/boards/{id}` - Get board details
- `PUT /api/v1/boards/{id}` - Update board (MANAGER/ADMIN)
- `DELETE /api/v1/boards/{id}` - Delete board (MANAGER/ADMIN)

### Tasks
- `GET /api/v1/tasks/board/{board_id}` - List tasks by board (with filters)
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get task details
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

### Comments
- `GET /api/v1/comments/task/{task_id}` - List comments by task
- `POST /api/v1/comments` - Create comment
- `GET /api/v1/comments/{id}` - Get comment details
- `PUT /api/v1/comments/{id}` - Update own comment
- `DELETE /api/v1/comments/{id}` - Delete own comment

## Security

- Password hashing with bcrypt
- JWT token expiration & rotation
- SQL injection protection via SQLAlchemy
- CORS configuration
- Rate limiting (planned)

## Database Management

### Access PostgreSQL Container
```bash
# Using container name
docker exec -it saas_postgres psql -U saas_user -d saas_db

# Using container ID
docker ps  # Get container ID
docker exec -it <container_id> psql -U saas_user -d saas_db
```

### Common PostgreSQL Commands
```sql
\l                    -- List databases
\dt                   -- List tables
\d+ table_name        -- Describe table
SELECT * FROM users;  -- Query data
\q                    -- Exit
```

### Backup and Restore
```bash
# Backup
docker exec saas_postgres pg_dump -U saas_user saas_db > backup.sql

# Restore
docker exec -i saas_postgres psql -U saas_user -d saas_db < backup.sql
```

### Reset Database
```bash
# Stop and remove volumes (deletes all data)
docker-compose down -v

# Start fresh
docker-compose up
docker exec -it saas_backend python scripts/init_db.py
docker exec -it saas_backend python scripts/seed_data.py
```

## Data Model

### Hierarchy
```
Organization (Tenant)
  └── Users (with Roles)
  └── Projects
      └── Boards (e.g., Sprint 1, Backlog)
          └── Tasks (with Status, Priority)
              └── Comments
```

### Task Statuses
- `TODO` - Not started
- `IN_PROGRESS` - Currently being worked on
- `IN_REVIEW` - Under review
- `DONE` - Completed
- `BLOCKED` - Blocked by dependencies

### Task Priorities
- `LOW` - Low priority
- `MEDIUM` - Medium priority
- `HIGH` - High priority
- `URGENT` - Urgent priority

## Deployment

Docker configuration included. See `docker-compose.yml` for details.

```bash
# Production deployment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```