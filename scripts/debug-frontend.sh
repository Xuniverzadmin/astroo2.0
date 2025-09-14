#!/bin/bash

# AstroOverz Frontend Debug Script
# This script helps debug the React frontend

echo "🔍 AstroOverz Frontend Debug Script"
echo "==================================="

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Check if port 5173 is available
echo "🔌 Checking port 5173..."
if lsof -i :5173 >/dev/null 2>&1; then
    echo "⚠️  Port 5173 is already in use. Attempting to kill existing process..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        taskkill /F /IM node.exe 2>/dev/null || true
    else
        pkill -f "vite.*5173" 2>/dev/null || true
    fi
    sleep 2
fi

# Set environment variables
export NODE_ENV=development
export VITE_API_URL=http://localhost:8000

echo "🚀 Starting React frontend in debug mode..."
echo "   - Frontend URL: http://localhost:5173"
echo "   - API URL: $VITE_API_URL"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the frontend
cd frontend
npm run dev

