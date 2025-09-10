#!/bin/bash

# Check Containers and Images on VPS
# Run this script on your VPS to see container status and image timestamps

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[INFO]${NC} Checking Docker containers and images..."

echo ""
echo "=========================================="
echo -e "${BLUE}[INFO]${NC} Docker Compose Services Status:"
echo "=========================================="

# Check containers
docker compose ps

echo ""
echo "=========================================="
echo -e "${BLUE}[INFO]${NC} Docker Images (with timestamps):"
echo "=========================================="

# Check images with timestamps
docker image ls | head

echo ""
echo "=========================================="
echo -e "${BLUE}[INFO]${NC} All Docker Images (full list):"
echo "=========================================="

# Show all images
docker image ls

echo ""
echo "=========================================="
echo -e "${BLUE}[INFO]${NC} Container Resource Usage:"
echo "=========================================="

# Check container resource usage
docker stats --no-stream

echo ""
echo "=========================================="
echo -e "${BLUE}[INFO]${NC} Recent Container Logs:"
echo "=========================================="

# Show recent logs
docker compose logs --tail=10

echo ""
echo -e "${GREEN}[SUCCESS]${NC} Container and image check completed!"
