# Multi-Tenant SaaS Project Management Platform

A production-ready, multi-tenant Saaas platform built with FastAPI, React, and PostgreSQL.

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
- React
- JWT Authentication
- Role-based UI

## Architecture

```
React → FastAPI → Services → SQLAlchemy → PostgreSQL
```

## Quick Start

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

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs

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
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh access token

### Organizations
- `GET /api/v1/organizations` - List organizations
- `POST /api/v1/organizations` - Create organization
- `GET /api/v1/organizations/{id}` - Get organization

### Projects
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/{id}` - Get project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

## Security

- Password hashing with bcrypt
- JWT token expiration & rotation
- SQL injection protection via SQLAlchemy
- CORS configuration
- Rate limiting (planned)

## Deployment

Docker configuration included. See `docker-compose.yml` for details.

```bash
docker-compose up -d
```

## License

MIT
