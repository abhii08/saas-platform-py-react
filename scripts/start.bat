@echo off
echo Starting Multi-Tenant SaaS Platform...

if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please update .env with your configuration!
)

echo Installing dependencies...
pip install -r requirements.txt

echo Initializing database...
python scripts\init_db.py

echo Seeding sample data...
python scripts\seed_data.py

echo Starting FastAPI server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
