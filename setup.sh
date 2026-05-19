#!/bin/bash

# Quick Start Script for CRM HCP System

echo "🚀 Starting AI-First CRM HCP Module..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi

# Check Node.js
echo -e "${BLUE}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null
then
    echo "Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

# Backend Setup
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    echo "⚠️  Please update .env with your GROQ_API_KEY and DATABASE_URL"
fi

echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo -e "${BLUE}To start backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload${NC}"

# Frontend Setup
echo -e "${BLUE}Setting up Frontend...${NC}"
cd ../frontend
npm install

if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
fi

echo -e "${GREEN}✅ Frontend setup complete!${NC}"
echo -e "${BLUE}To start frontend: cd frontend && npm start${NC}"

echo -e "${GREEN}🎉 Setup complete! Both services are ready to run.${NC}"
echo -e "${BLUE}Backend: http://localhost:8000${NC}"
echo -e "${BLUE}Frontend: http://localhost:3000${NC}"
