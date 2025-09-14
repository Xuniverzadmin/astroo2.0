@echo off
REM AstroOverz Full Stack Debug Script for Windows
REM This script starts both backend and frontend for debugging

echo 🔍 AstroOverz Full Stack Debug Script
echo =====================================

REM Check if we're in the right directory
if not exist "backend\numerology_app\main.py" (
    echo ❌ Error: Backend not found. Please run from project root.
    pause
    exit /b 1
)
if not exist "frontend\package.json" (
    echo ❌ Error: Frontend not found. Please run from project root.
    pause
    exit /b 1
)

REM Check virtual environment
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

REM Install backend dependencies if needed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing backend dependencies...
    pip install -r backend\requirements.txt
)

REM Install frontend dependencies if needed
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

REM Set environment variables
set PYTHONPATH=%CD%\backend
set DATABASE_URL=postgresql://astroz:Vettri2025@localhost:5432/astrooverz
set REDIS_URL=redis://localhost:6379/0
set SECRET_KEY=change_me_to_a_random_32_chars_minimum_length_here
set NODE_ENV=development
set VITE_API_URL=http://localhost:8000

REM Kill any existing processes on ports 8000 and 5173
echo 🔌 Cleaning up existing processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 >nul

echo 🚀 Starting full stack debug environment...
echo.
echo 📡 Services:
echo    - Backend API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo    - Frontend: http://localhost:5173
echo    - Health Check: http://localhost:8000/health
echo.
echo 🔧 Debug Tools:
echo    - REST Client: api_test.rest
echo    - VS Code Debugger: F5 to start debugging
echo    - Browser DevTools: F12
echo.
echo Press Ctrl+C to stop all services
echo.

REM Start backend in background
echo 🖥️  Starting backend...
cd backend
start "Backend" cmd /k "uvicorn numerology_app.api:app --reload --host 0.0.0.0 --port 8000 --log-level debug"
cd ..

REM Wait a moment for backend to start
timeout /t 3 >nul

REM Start frontend in background
echo 🌐 Starting frontend...
cd frontend
start "Frontend" cmd /k "npm run dev"
cd ..

echo ✅ Both services started successfully!
echo.
echo 🔍 Debugging Tips:
echo    1. Open http://localhost:5173 in your browser
echo    2. Open DevTools (F12) to see console logs
echo    3. Use api_test.rest to test API endpoints
echo    4. Set breakpoints in VS Code and press F5 to debug
echo.
echo Press any key to exit...
pause >nul

