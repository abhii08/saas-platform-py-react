# Multi-Tenant SaaS Platform - Setup Guide

This guide will help you set up and run the Multi-Tenant SaaS Project Management Platform.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

## Quick Start with Docker (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# Start all services (PostgreSQL, Backend)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## Manual Setup

### 1. Backend Setup

#### Create Virtual Environment

```bash
# Navigate to project root
cd c:\Users\ABHIN\Projects\Python\SaaS-Platform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and update these values:
# - DATABASE_URL: Your PostgreSQL connection string
# - SECRET_KEY: Generate a secure random key
```

**Generate a secure SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

#### Setup Database

**Option 1: Using PostgreSQL locally**

```bash
# Create database
psql -U postgres
CREATE DATABASE saas_db;
CREATE USER saas_user WITH PASSWORD 'saas_password';
GRANT ALL PRIVILEGES ON DATABASE saas_db TO saas_user;
\q

# Update .env
DATABASE_URL=postgresql://saas_user:saas_password@localhost:5432/saas_db
```

**Option 2: Using Docker for PostgreSQL only**

```bash
docker run -d \
  --name saas_postgres \
  -e POSTGRES_USER=saas_user \
  -e POSTGRES_PASSWORD=saas_password \
  -e POSTGRES_DB=saas_db \
  -p 5432:5432 \
  postgres:15-alpine
```

#### Initialize Database

```bash
# Initialize database tables and default roles
python scripts/init_db.py

# (Optional) Seed sample data for testing
python scripts/seed_data.py
```

#### Run Backend Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: http://localhost:5173

## Testing the Application

### Using Sample Data

If you ran `python scripts/seed_data.py`, you can login with:

- **Admin**: admin@acme.com / password123
- **Manager**: manager@acme.com / password123
- **Member**: member@acme.com / password123

### Creating a New Account

1. Navigate to http://localhost:5173/register
2. Fill in the registration form:
   - Email: your@email.com
   - Password: (minimum 8 characters)
   - Organization Name: Your Company
   - Organization Slug: your-company
3. Click "Create account"
4. You'll be automatically logged in as ORG_ADMIN

### API Testing

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

**Example API calls:**

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User",
    "organization_name": "Test Org",
    "organization_slug": "test-org"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Use the access_token from login response for authenticated requests
curl -X GET http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

```
SaaS-Platform/
├── app/                      # Backend application
│   ├── main.py              # FastAPI app entry point
│   ├── core/                # Core configuration
│   │   ├── config.py       # Settings
│   │   ├── security.py     # JWT & password utilities
│   │   └── dependencies.py # Auth dependencies
│   ├── auth/               # Authentication module
│   ├── organizations/      # Organization management
│   ├── users/              # User management
│   ├── projects/           # Project management
│   ├── boards/             # Board management
│   ├── tasks/              # Task management
│   ├── comments/           # Comment management
│   ├── roles/              # Role management
│   ├── database/           # Database configuration
│   └── utils/              # Utilities
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # Reusable components
│   │   ├── context/       # React context
│   │   ├── pages/         # Page components
│   │   └── App.jsx        # Main app
│   └── package.json
├── scripts/               # Utility scripts
│   ├── init_db.py        # Database initialization
│   └── seed_data.py      # Sample data seeding
├── tests/                # Backend tests
├── alembic/              # Database migrations
├── docker-compose.yml    # Docker configuration
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Key Features Implemented

### Multi-Tenancy
- ✅ Shared database with tenant isolation
- ✅ Every query scoped to organization_id
- ✅ Automatic tenant extraction from JWT

### Authentication & Authorization
- ✅ JWT-based authentication (access + refresh tokens)
- ✅ Password hashing with bcrypt
- ✅ Role-based access control (RBAC)
- ✅ Three roles: ORG_ADMIN, PROJECT_MANAGER, MEMBER

### API Endpoints
- ✅ `/api/v1/auth/*` - Authentication
- ✅ `/api/v1/organizations/*` - Organization management
- ✅ `/api/v1/projects/*` - Project management
- ✅ `/api/v1/boards/*` - Board management
- ✅ `/api/v1/tasks/*` - Task management
- ✅ `/api/v1/comments/*` - Comment management

### Frontend
- ✅ React with React Router
- ✅ JWT authentication flow
- ✅ Protected routes
- ✅ Role-based UI
- ✅ Responsive design with Tailwind CSS

## Development Workflow

### Running Tests

```bash
# Backend tests
pytest

# Run specific test file
pytest tests/test_auth.py

# With coverage
pytest --cov=app tests/
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## Production Deployment

### Environment Variables

Ensure these are set in production:

```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=<strong-random-key>
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com
```

### Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Use HTTPS/TLS for all connections
- [ ] Set strong database passwords
- [ ] Configure CORS for your domain only
- [ ] Enable rate limiting
- [ ] Set up database backups
- [ ] Use environment variables for secrets
- [ ] Enable PostgreSQL SSL connections
- [ ] Configure firewall rules

### Deployment Options

**Option 1: Docker**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Option 2: Traditional Server**
- Use Nginx as reverse proxy
- Run backend with Gunicorn/Uvicorn workers
- Serve frontend as static files
- Use systemd for process management

**Option 3: Cloud Platforms**
- AWS: ECS/Fargate + RDS + S3
- Google Cloud: Cloud Run + Cloud SQL
- Azure: App Service + Azure Database
- Heroku: Web dyno + Postgres addon

## Troubleshooting

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U saas_user -d saas_db -h localhost

# Check if PostgreSQL is running
# Windows:
sc query postgresql-x64-15
# Linux:
systemctl status postgresql
```

### Port Already in Use

```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
# Linux:
lsof -i :8000

# Kill the process
# Windows:
taskkill /PID <PID> /F
# Linux:
kill -9 <PID>
```

### Frontend Build Issues

```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. **Add More Features**
   - File uploads for tasks
   - Real-time notifications with WebSockets
   - Email notifications
   - Activity logs/audit trail
   - Advanced search and filtering

2. **Enhance Security**
   - Implement rate limiting
   - Add OAuth providers (Google, GitHub)
   - Two-factor authentication
   - API key management

3. **Performance Optimization**
   - Database query optimization
   - CDN for static assets
   - Implement caching strategies
   - Background job processing

4. **Monitoring & Logging**
   - Set up application monitoring (Sentry, DataDog)
   - Centralized logging (ELK stack)
   - Performance metrics
   - Health checks

## Support

For issues or questions:
- Check the API documentation at `/docs`
- Review the code comments and docstrings
- Refer to FastAPI documentation: https://fastapi.tiangolo.com
- React documentation: https://react.dev

## License

MIT License - Feel free to use this project for learning and commercial purposes.
