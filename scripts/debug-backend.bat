@echo off
REM AstroOverz Backend Debug Script for Windows
REM This script helps debug the FastAPI backend

echo 🔍 AstroOverz Backend Debug Script
echo ==================================

REM Check if we're in the right directory
if not exist "backend\numerology_app\main.py" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo ❌ Error: Virtual environment not found. Please create one first:
    echo    python -m venv .venv
    echo    .venv\Scripts\activate
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if dependencies are installed
echo 📦 Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo ❌ FastAPI not found. Installing dependencies...
    pip install -r backend\requirements.txt
)

REM Check if port 8000 is available
echo 🔌 Checking port 8000...
netstat -an | findstr :8000 >nul
if not errorlevel 1 (
    echo ⚠️  Port 8000 is already in use. Attempting to kill existing process...
    taskkill /F /IM python.exe >nul 2>&1
    timeout /t 2 >nul
)

REM Set environment variables
set PYTHONPATH=%CD%\backend
set DATABASE_URL=postgresql://astroz:Vettri2025@localhost:5432/astrooverz
set REDIS_URL=redis://localhost:6379/0
set SECRET_KEY=change_me_to_a_random_32_chars_minimum_length_here

REM Check if OpenAI API key is set
if "%OPENAI_API_KEY%"=="" (
    echo ⚠️  OPENAI_API_KEY not set. Some features may not work.
    echo    Set it with: set OPENAI_API_KEY=your_key_here
)

echo 🚀 Starting FastAPI backend in debug mode...
echo    - Backend URL: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo    - Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the backend with debug logging
cd backend
uvicorn numerology_app.api:app --reload --host 0.0.0.0 --port 8000 --log-level debug

