#!/bin/bash

# Simple rebuild script - exactly as requested
# This script performs the exact commands you specified

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[INFO]${NC} Starting clean rebuild process..."

# Navigate to project directory
cd /opt/astrooverz || cd /opt/astro2.0 || cd /opt/astrooerz

echo -e "${BLUE}[INFO]${NC} Pulling latest images..."
docker compose pull || true        # pulls if you have a registry; safe to run

echo -e "${BLUE}[INFO]${NC} Building containers with new code..."
docker compose build --no-cache    # force rebuild with new code

echo -e "${BLUE}[INFO]${NC} Starting services..."
docker compose up -d --remove-orphans

echo -e "${GREEN}[SUCCESS]${NC} Rebuild completed successfully!"

# Show status
echo -e "${BLUE}[INFO]${NC} Service status:"
docker compose ps

# Wait a moment and check health
echo -e "${BLUE}[INFO]${NC} Waiting for services to be ready..."
sleep 30

# Quick health check
if curl -f http://localhost:8000/healthz >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} Backend is healthy"
else
    echo -e "${YELLOW}[WARNING]${NC} Backend health check failed - services may still be starting"
fi

if curl -f http://localhost:8000/api/healthz >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} API is healthy"
else
    echo -e "${YELLOW}[WARNING]${NC} API health check failed - services may still be starting"
fi

echo -e "${GREEN}[SUCCESS]${NC} Rebuild process completed!"
echo -e "${BLUE}[INFO]${NC} You can check logs with: docker compose logs -f"
echo -e "${BLUE}[INFO]${NC} You can check status with: docker compose ps"
