#!/bin/bash

# AstroOverz Backend Debug Script
# This script helps debug the FastAPI backend

echo "🔍 AstroOverz Backend Debug Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "backend/numerology_app/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
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

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI not found. Installing dependencies..."
    pip install -r backend/requirements.txt
fi

# Check if port 8000 is available
echo "🔌 Checking port 8000..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo "⚠️  Port 8000 is already in use. Attempting to kill existing process..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        taskkill /F /IM python.exe 2>/dev/null || true
    else
        pkill -f "uvicorn.*8000" 2>/dev/null || true
    fi
    sleep 2
fi

# Set environment variables
export PYTHONPATH="${PWD}/backend"
export DATABASE_URL="postgresql://astroz:Vettri2025@localhost:5432/astrooverz"
export REDIS_URL="redis://localhost:6379/0"
export SECRET_KEY="change_me_to_a_random_32_chars_minimum_length_here"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set. Some features may not work."
    echo "   Set it with: export OPENAI_API_KEY=your_key_here"
fi

echo "🚀 Starting FastAPI backend in debug mode..."
echo "   - Backend URL: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the backend with debug logging
cd backend
uvicorn numerology_app.api:app --reload --host 0.0.0.0 --port 8000 --log-level debug

