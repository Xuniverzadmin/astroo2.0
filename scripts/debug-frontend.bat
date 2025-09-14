@echo off
REM AstroOverz Frontend Debug Script for Windows
REM This script helps debug the React frontend

echo 🔍 AstroOverz Frontend Debug Script
echo ===================================

REM Check if we're in the right directory
if not exist "frontend\package.json" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

REM Check if port 5173 is available
echo 🔌 Checking port 5173...
netstat -an | findstr :5173 >nul
if not errorlevel 1 (
    echo ⚠️  Port 5173 is already in use. Attempting to kill existing process...
    taskkill /F /IM node.exe >nul 2>&1
    timeout /t 2 >nul
)

REM Set environment variables
set NODE_ENV=development
set VITE_API_URL=http://localhost:8000

echo 🚀 Starting React frontend in debug mode...
echo    - Frontend URL: http://localhost:5173
echo    - API URL: %VITE_API_URL%
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the frontend
cd frontend
npm run dev

