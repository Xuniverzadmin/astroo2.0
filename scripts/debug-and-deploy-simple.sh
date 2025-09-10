#!/bin/bash

# Simple Debug and Deploy Script
# This script runs the exact commands you specified

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
VPS_IP="${VPS_IP:-}"

echo -e "${BLUE}[INFO]${NC} Debug and Deploy Script for Astrooverz"

# Check if VPS_IP is set
if [ -z "$VPS_IP" ]; then
    echo -e "${YELLOW}[WARNING]${NC} VPS_IP environment variable is not set"
    echo -e "${BLUE}[INFO]${NC} Please set VPS_IP before running this script:"
    echo -e "${BLUE}[INFO]${NC} export VPS_IP=your_vps_ip_address"
    exit 1
fi

echo -e "${BLUE}[INFO]${NC} VPS IP: $VPS_IP"

# Step 1: SSH to VPS and find project directory
echo -e "${BLUE}[INFO]${NC} Step 1: Finding project directory..."
echo "Command: ssh root@$VPS_IP"

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

# Step 2: Check git status (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 2: Checking git status..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && git status'"

if ssh root@$VPS_IP "cd $PROJECT_DIR && git status"; then
    echo -e "${GREEN}[SUCCESS]${NC} Git status checked successfully"
else
    echo -e "${YELLOW}[WARNING]${NC} Git status check failed"
fi

echo ""

# Step 3: Fetch latest changes (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 3: Fetching latest changes..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && git fetch --all'"

if ssh root@$VPS_IP "cd $PROJECT_DIR && git fetch --all"; then
    echo -e "${GREEN}[SUCCESS]${NC} Latest changes fetched successfully"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to fetch latest changes"
fi

echo ""

# Step 4: Get current commit hash (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Step 4: Getting current commit hash..."
echo "Command: ssh root@$VPS_IP 'cd $PROJECT_DIR && git rev-parse --short HEAD'"

if current_commit=$(ssh root@$VPS_IP "cd $PROJECT_DIR && git rev-parse --short HEAD"); then
    echo -e "${GREEN}[SUCCESS]${NC} Current commit hash: $current_commit"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to get current commit hash"
fi

echo ""

# Step 5: Get local commit hash for comparison
echo -e "${BLUE}[INFO]${NC} Step 5: Getting local commit hash for comparison..."
echo "Command: git rev-parse --short HEAD"

if local_commit=$(git rev-parse --short HEAD); then
    echo -e "${GREEN}[SUCCESS]${NC} Local commit hash: $local_commit"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to get local commit hash"
fi

echo ""

# Step 6: Compare commit hashes
echo -e "${BLUE}[INFO]${NC} Step 6: Comparing commit hashes..."
if [ "$current_commit" = "$local_commit" ]; then
    echo -e "${GREEN}[SUCCESS]${NC} Commit hashes match: $current_commit"
else
    echo -e "${YELLOW}[WARNING]${NC} Commit hashes do not match:"
    echo -e "${YELLOW}[WARNING]${NC}   Local:  $local_commit"
    echo -e "${YELLOW}[WARNING]${NC}   Remote: $current_commit"
fi

echo ""

# Additional debugging steps
echo -e "${BLUE}[INFO]${NC} Additional debugging steps..."

# Check environment file
echo -e "${BLUE}[INFO]${NC} Checking environment file..."
if ssh root@$VPS_IP "cd $PROJECT_DIR && ls -la .env .env.sample"; then
    echo -e "${GREEN}[SUCCESS]${NC} Environment files found"
else
    echo -e "${YELLOW}[WARNING]${NC} Environment files not found"
fi

echo ""

# Check Docker services
echo -e "${BLUE}[INFO]${NC} Checking Docker services..."
if ssh root@$VPS_IP "cd $PROJECT_DIR && docker compose ps"; then
    echo -e "${GREEN}[SUCCESS]${NC} Docker services status checked"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to check Docker services"
fi

echo ""

# Check Docker logs
echo -e "${BLUE}[INFO]${NC} Checking Docker logs..."
if ssh root@$VPS_IP "cd $PROJECT_DIR && docker compose logs --tail=10"; then
    echo -e "${GREEN}[SUCCESS]${NC} Docker logs checked"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to check Docker logs"
fi

echo ""

# Test endpoints
echo -e "${BLUE}[INFO]${NC} Testing endpoints..."

# Test backend health
if ssh root@$VPS_IP "cd $PROJECT_DIR && curl -s http://backend:8000/healthz"; then
    echo -e "${GREEN}[SUCCESS]${NC} Backend health check passed"
else
    echo -e "${YELLOW}[WARNING]${NC} Backend health check failed"
fi

# Test API health
if ssh root@$VPS_IP "cd $PROJECT_DIR && curl -s http://backend:8000/api/healthz"; then
    echo -e "${GREEN}[SUCCESS]${NC} API health check passed"
else
    echo -e "${YELLOW}[WARNING]${NC} API health check failed"
fi

# Test panchangam API
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
echo -e "${BLUE}[INFO]${NC} Debug and deploy summary:"
echo -e "${BLUE}[INFO]${NC}   Project directory: $PROJECT_DIR"
echo -e "${BLUE}[INFO]${NC}   Local commit: $local_commit"
echo -e "${BLUE}[INFO]${NC}   Remote commit: $current_commit"
echo -e "${BLUE}[INFO]${NC}   Commit match: $([ "$current_commit" = "$local_commit" ] && echo "Yes" || echo "No")"

echo ""
echo -e "${GREEN}[SUCCESS]${NC} Debug and deploy completed!"
echo -e "${BLUE}[INFO]${NC} You can run individual commands:"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && git status'"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && git fetch --all'"
echo "  ssh root@$VPS_IP 'cd $PROJECT_DIR && git rev-parse --short HEAD'"
