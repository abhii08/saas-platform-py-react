#!/bin/bash

echo "Starting Multi-Tenant SaaS Platform..."

if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env with your configuration!"
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python scripts/init_db.py

echo "Seeding sample data..."
python scripts/seed_data.py

echo "Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
