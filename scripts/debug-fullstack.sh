#!/bin/bash

# AstroOverz Full Stack Debug Script
# This script starts both backend and frontend for debugging

echo "🔍 AstroOverz Full Stack Debug Script"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "backend/numerology_app/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        taskkill /F /IM python.exe 2>/dev/null || true
        taskkill /F /IM node.exe 2>/dev/null || true
    else
        pkill -f "uvicorn.*8000" 2>/dev/null || true
        pkill -f "vite.*5173" 2>/dev/null || true
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Please create one first:"
    echo "   python -m venv .venv"
    echo "   . .venv/Scripts/activate  # Windows"
    echo "   source .venv/bin/activate  # Mac/Linux"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install backend dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing backend dependencies..."
    pip install -r backend/requirements.txt
fi

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Set environment variables
export PYTHONPATH="${PWD}/backend"
export DATABASE_URL="postgresql://astroz:Vettri2025@localhost:5432/astrooverz"
export REDIS_URL="redis://localhost:6379/0"
export SECRET_KEY="change_me_to_a_random_32_chars_minimum_length_here"
export NODE_ENV=development
export VITE_API_URL=http://localhost:8000

# Kill any existing processes on ports 8000 and 5173
echo "🔌 Cleaning up existing processes..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    taskkill /F /IM python.exe 2>/dev/null || true
    taskkill /F /IM node.exe 2>/dev/null || true
else
    pkill -f "uvicorn.*8000" 2>/dev/null || true
    pkill -f "vite.*5173" 2>/dev/null || true
fi
sleep 2

echo "🚀 Starting full stack debug environment..."
echo ""
echo "📡 Services:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Frontend: http://localhost:5173"
echo "   - Health Check: http://localhost:8000/health"
echo ""
echo "🔧 Debug Tools:"
echo "   - REST Client: api_test.rest"
echo "   - VS Code Debugger: F5 to start debugging"
echo "   - Browser DevTools: F12"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start backend in background
echo "🖥️  Starting backend..."
cd backend
uvicorn numerology_app.api:app --reload --host 0.0.0.0 --port 8000 --log-level debug &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "🌐 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for both processes
echo "✅ Both services started successfully!"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "🔍 Debugging Tips:"
echo "   1. Open http://localhost:5173 in your browser"
echo "   2. Open DevTools (F12) to see console logs"
echo "   3. Use api_test.rest to test API endpoints"
echo "   4. Set breakpoints in VS Code and press F5 to debug"
echo ""

# Wait for user to stop
wait

