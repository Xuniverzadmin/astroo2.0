#!/bin/bash

# Simple Clean Rebuild and Restart Script
# This script runs the exact commands you specified

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
VPS_IP="${VPS_IP:-}"

echo -e "${BLUE}[INFO]${NC} Clean Rebuild and Restart Script for Astrooverz"

# Check if VPS_IP is set
if [ -z "$VPS_IP" ]; then
    echo -e "${YELLOW}[WARNING]${NC} VPS_IP environment variable is not set"
    echo -e "${BLUE}[INFO]${NC} Please set VPS_IP before running this script:"
    echo -e "${BLUE}[INFO]${NC} export VPS_IP=your_vps_ip_address"
    exit 1
fi

echo -e "${BLUE}[INFO]${NC} VPS IP: $VPS_IP"

# Find the correct project directory
PROJECT_DIR=""
for dir in "/opt/astrooverz" "/opt/astroo2.0" "/opt/astrooerz"; do
    if ssh root@$VPS_IP "test -d $dir" 2>/dev/null; then
        PROJECT_DIR="$dir"
        echo -e "${GREEN}[SUCCESS]${NC} Found project directory: $PROJECT_DIR"
        break
    fi
done

if [ -z "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Could not find project directory in /opt/astrooverz, /opt/astroo2.0, or /opt/astrooerz"
    echo -e "${BLUE}[INFO]${NC} Please check the project directory manually"
    exit 1
fi

echo ""

# Step 1: Pull latest changes (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 1: Pulling latest changes..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && git pull --rebase'"

if ssh root@$VPS_IP "cd $PROJECT_DIR && git pull --rebase"; then
    echo -e "${GREEN}[SUCCESS]${NC} Latest changes pulled successfully"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to pull latest changes"
fi

echo ""

# Step 2: Stop all services (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 2: Stopping all services..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose down'"

if ssh root@$VPS_IP "cd $PROJECT_DIR && docker compose down"; then
    echo -e "${GREEN}[SUCCESS]${NC} All services stopped successfully"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to stop services"
fi

echo ""

# Step 3: Build containers (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 3: Building containers with no cache..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose build --no-cache'"

if ssh root@$VPS_IP "cd $PROJECT_DIR && docker compose build --no-cache"; then
    echo -e "${GREEN}[SUCCESS]${NC} Containers built successfully"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to build containers"
fi

echo ""

# Step 4: Start services (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 4: Starting services..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose up -d --remove-orphans'"

if ssh root@$VPS_IP "cd $PROJECT_DIR && docker compose up -d --remove-orphans"; then
    echo -e "${GREEN}[SUCCESS]${NC} Services started successfully"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to start services"
fi

echo ""

# Step 5: Check service status (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 5: Checking service status..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose ps'"

if ssh root@$VPS_IP "cd $PROJECT_DIR && docker compose ps"; then
    echo -e "${GREEN}[SUCCESS]${NC} Service status checked"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to check service status"
fi

echo ""

# Additional verification steps
echo -e "${BLUE}[INFO]${NC} Additional verification steps..."

# Test backend health
echo -e "${BLUE}[INFO]${NC} Testing backend health..."
if ssh root@$VPS_IP "cd $PROJECT_DIR && curl -s http://backend:8000/healthz"; then
    echo -e "${GREEN}[SUCCESS]${NC} Backend health check passed"
else
    echo -e "${YELLOW}[WARNING]${NC} Backend health check failed"
fi

# Test API health
echo -e "${BLUE}[INFO]${NC} Testing API health..."
if ssh root@$VPS_IP "cd $PROJECT_DIR && curl -s http://backend:8000/api/healthz"; then
    echo -e "${GREEN}[SUCCESS]${NC} API health check passed"
else
    echo -e "${YELLOW}[WARNING]${NC} API health check failed"
fi

# Test panchangam API
echo -e "${BLUE}[INFO]${NC} Testing panchangam API..."
if ssh root@$VPS_IP "cd $PROJECT_DIR && curl -s 'http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400"; then
    echo -e "${GREEN}[SUCCESS]${NC} Panchangam API test passed"
else
    echo -e "${YELLOW}[WARNING]${NC} Panchangam API test failed"
fi

echo ""

# Test public domain
echo -e "${BLUE}[INFO]${NC} Testing public domain..."

# Test homepage
if curl -I https://www.astrooverz.com >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} Homepage is accessible"
else
    echo -e "${YELLOW}[WARNING]${NC} Homepage test failed"
fi

# Test API health
if curl -s https://www.astrooverz.com/api/healthz >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} API health endpoint is accessible"
else
    echo -e "${YELLOW}[WARNING]${NC} API health endpoint test failed"
fi

# Test panchangam API
if curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} Panchangam API is accessible"
else
    echo -e "${YELLOW}[WARNING]${NC} Panchangam API test failed"
fi

echo ""

# Summary
echo -e "${BLUE}[INFO]${NC} Clean rebuild and restart summary:"
echo -e "${BLUE}[INFO]${NC}   Project directory: $PROJECT_DIR"
echo -e "${BLUE}[INFO]${NC}   Services: Stopped, Built, Started"
echo -e "${BLUE}[INFO]${NC}   Status: Checked"

echo ""
echo -e "${GREEN}[SUCCESS]${NC} Clean rebuild and restart completed!"
echo -e "${BLUE}[INFO]${NC} You can run individual commands:"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && git pull --rebase'"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose down'"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose build --no-cache'"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose up -d --remove-orphans'"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && docker compose ps'"
