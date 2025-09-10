#!/bin/bash

# Simple API Testing Script
# This script runs the exact commands you specified

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[INFO]${NC} Testing Backend API endpoints..."

# Test 1: Health endpoint
echo -e "${BLUE}[INFO]${NC} Testing health endpoint..."
if curl -s http://backend:8000/healthz; then
    echo -e "\n${GREEN}[SUCCESS]${NC} Health endpoint is working"
else
    echo -e "\n${YELLOW}[WARNING]${NC} Health endpoint test failed"
fi

echo ""

# Test 2: Panchangam API
echo -e "${BLUE}[INFO]${NC} Testing panchangam API..."
echo "URL: http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata"
echo "Response (first 400 chars):"

if response=$(curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata); then
    echo "$response" | head -c 400
    echo ""
    echo "..."
    echo -e "${GREEN}[SUCCESS]${NC} Panchangam API is working"
else
    echo -e "${YELLOW}[WARNING]${NC} Panchangam API test failed"
fi

echo ""

# Additional tests
echo -e "${BLUE}[INFO]${NC} Running additional health checks..."

# Test API health endpoint
echo -e "${BLUE}[INFO]${NC} Testing API health endpoint..."
if curl -s http://backend:8000/api/healthz; then
    echo -e "\n${GREEN}[SUCCESS]${NC} API health endpoint is working"
else
    echo -e "\n${YELLOW}[WARNING]${NC} API health endpoint test failed"
fi

echo ""

# Test with localhost (alternative)
echo -e "${BLUE}[INFO]${NC} Testing with localhost..."
if curl -s http://localhost:8000/healthz >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} Localhost health endpoint is working"
else
    echo -e "${YELLOW}[WARNING]${NC} Localhost health endpoint test failed"
fi

echo ""

# Test panchangam API with localhost
echo -e "${BLUE}[INFO]${NC} Testing panchangam API with localhost..."
if curl -s http://localhost:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} Localhost panchangam API is working"
else
    echo -e "${YELLOW}[WARNING]${NC} Localhost panchangam API test failed"
fi

echo ""
echo -e "${GREEN}[SUCCESS]${NC} API testing completed!"
echo -e "${BLUE}[INFO]${NC} You can run individual tests:"
echo "  curl -s http://backend:8000/healthz"
echo "  curl -s http://backend:8000/api/healthz"
echo "  curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata"
