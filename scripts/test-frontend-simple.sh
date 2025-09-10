#!/bin/bash

# Simple Frontend Testing Script
# This script runs the exact command you specified

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[INFO]${NC} Testing Frontend serving through Caddy..."

# Test 1: Frontend through Caddy (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Testing frontend through Caddy (exact command)..."
echo "Command: docker compose exec caddy sh -lc 'wget -qO- http://frontend:80 | head -n 20'"

if response=$(docker compose exec caddy sh -lc 'wget -qO- http://frontend:80 | head -n 20' 2>/dev/null); then
    echo -e "${GREEN}[SUCCESS]${NC} Frontend is serving through Caddy"
    echo "Response (first 20 lines):"
    echo "$response"
else
    echo -e "${YELLOW}[WARNING]${NC} Frontend test through Caddy failed"
fi

echo ""

# Additional tests
echo -e "${BLUE}[INFO]${NC} Running additional frontend tests..."

# Test 2: Frontend service directly
echo -e "${BLUE}[INFO]${NC} Testing frontend service directly..."
if docker compose exec frontend sh -c 'wget -qO- http://localhost:5173 | head -n 10' 2>/dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} Frontend service is working directly"
else
    echo -e "${YELLOW}[WARNING]${NC} Frontend service test failed"
fi

echo ""

# Test 3: Caddy serving frontend
echo -e "${BLUE}[INFO]${NC} Testing Caddy serving frontend..."
if docker compose exec caddy sh -c 'wget -qO- http://localhost:80 | head -n 10' 2>/dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} Caddy is serving frontend"
else
    echo -e "${YELLOW}[WARNING]${NC} Caddy serving test failed"
fi

echo ""

# Test 4: External access
echo -e "${BLUE}[INFO]${NC} Testing external access..."
if curl -s http://localhost:80 | head -n 10 >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} External access to frontend is working"
else
    echo -e "${YELLOW}[WARNING]${NC} External access test failed"
fi

echo ""

# Test 5: API proxy through Caddy
echo -e "${BLUE}[INFO]${NC} Testing API proxy through Caddy..."
if curl -s http://localhost:80/api/healthz >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} API proxy through Caddy is working"
else
    echo -e "${YELLOW}[WARNING]${NC} API proxy test failed"
fi

echo ""

# Show service status
echo -e "${BLUE}[INFO]${NC} Service status:"
docker compose ps frontend caddy

echo ""
echo -e "${GREEN}[SUCCESS]${NC} Frontend testing completed!"
echo -e "${BLUE}[INFO]${NC} You can run individual tests:"
echo "  docker compose exec caddy sh -lc 'wget -qO- http://frontend:80 | head -n 20'"
echo "  docker compose exec frontend sh -c 'wget -qO- http://localhost:5173 | head -n 10'"
echo "  curl -s http://localhost:80 | head -n 10"
