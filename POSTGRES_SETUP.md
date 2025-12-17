# PostgreSQL Setup Guide for Windows

## Step 1: Install PostgreSQL

### Download PostgreSQL
1. Go to: https://www.postgresql.org/download/windows/
2. Click "Download the installer"
3. Download PostgreSQL 15 or 16 (recommended)

### Install PostgreSQL
1. Run the installer
2. **Important settings during installation:**
   - Installation Directory: Keep default (C:\Program Files\PostgreSQL\15)
   - Components: Select all (PostgreSQL Server, pgAdmin 4, Command Line Tools)
   - Data Directory: Keep default
   - **Password**: Set a password for the `postgres` superuser (REMEMBER THIS!)
   - Port: Keep default `5432`
   - Locale: Keep default

3. Complete the installation
4. Uncheck "Launch Stack Builder" at the end

## Step 2: Create Database

### Option A: Using pgAdmin (GUI)
1. Open pgAdmin 4 from Start Menu
2. Enter the password you set during installation
3. Right-click "Databases" → Create → Database
4. Database name: `saas_db`
5. Click "Save"

### Option B: Using Command Line (psql)
1. Open Command Prompt or PowerShell
2. Run these commands:

```bash
# Connect to PostgreSQL
psql -U postgres

# Enter your password when prompted

# Create database
CREATE DATABASE saas_db;

# Create user
CREATE USER saas_user WITH PASSWORD 'saas_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE saas_db TO saas_user;

# Exit
\q
```

## Step 3: Verify Installation

Test the connection:

```bash
psql -U postgres -d saas_db
```

If you see the PostgreSQL prompt, you're ready!

## Step 4: Update .env File

Your `.env` file should have:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/saas_db
```

Replace `YOUR_PASSWORD` with the password you set during installation.

## Troubleshooting

### "psql is not recognized"
Add PostgreSQL to PATH:
1. Search "Environment Variables" in Windows
2. Edit "Path" in System Variables
3. Add: `C:\Program Files\PostgreSQL\15\bin`
4. Restart terminal

### Connection refused
Make sure PostgreSQL service is running:
1. Open Services (Win + R, type `services.msc`)
2. Find "postgresql-x64-15"
3. Right-click → Start

## Next Steps

Once PostgreSQL is installed and running, return to the main terminal and run:

```bash
python scripts\init_db.py
python scripts\seed_data.py
uvicorn app.main:app --reload
```
