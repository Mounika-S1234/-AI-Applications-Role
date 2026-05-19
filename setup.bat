@echo off
REM CRM HCP System Setup Script for Windows

echo.
echo 🚀 Starting AI-First CRM HCP Module Setup...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+
    pause
    exit /b 1
)

REM Backend Setup
echo 📦 Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please update .env with your GROQ_API_KEY and DATABASE_URL
)

echo ✅ Backend setup complete!
echo To start backend: cd backend && venv\Scripts\activate.bat && uvicorn app.main:app --reload
echo.

REM Frontend Setup
echo 📦 Setting up Frontend...
cd ..\frontend
call npm install

if not exist ".env" (
    echo 📝 Creating .env file...
    echo REACT_APP_API_URL=http://localhost:8000/api > .env
)

echo ✅ Frontend setup complete!
echo To start frontend: cd frontend && npm start
echo.
echo 🎉 Setup complete! Both services are ready to run.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
