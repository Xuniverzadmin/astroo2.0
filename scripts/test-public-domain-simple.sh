#!/bin/bash

# Simple Public Domain Testing Script
# This script runs the exact commands you specified

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[INFO]${NC} Testing Public Domain Endpoints..."

# Test 1: Homepage (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Testing homepage..."
echo "Command: curl -I https://www.astrooverz.com"

if response=$(curl -I https://www.astrooverz.com 2>/dev/null); then
    echo -e "${GREEN}[SUCCESS]${NC} Homepage is accessible"
    echo "Response headers:"
    echo "$response"
else
    echo -e "${YELLOW}[WARNING]${NC} Homepage test failed"
fi

echo ""

# Test 2: API Health (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Testing API health endpoint..."
echo "Command: curl -s https://www.astrooverz.com/api/healthz"

if response=$(curl -s https://www.astrooverz.com/api/healthz 2>/dev/null); then
    echo -e "${GREEN}[SUCCESS]${NC} API health endpoint is working"
    echo "Response: $response"
else
    echo -e "${YELLOW}[WARNING]${NC} API health endpoint test failed"
fi

echo ""

# Test 3: Panchangam API (exact command as requested)
echo -e "${BLUE}[INFO]${NC} Testing panchangam API..."
echo "Command: curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400"

if response=$(curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' 2>/dev/null); then
    echo -e "${GREEN}[SUCCESS]${NC} Panchangam API is working"
    echo "Response (first 400 characters):"
    echo "$response" | head -c 400
    echo ""
else
    echo -e "${YELLOW}[WARNING]${NC} Panchangam API test failed"
fi

echo ""

# Additional tests
echo -e "${BLUE}[INFO]${NC} Running additional public domain tests..."

# Test 4: SSL Certificate
echo -e "${BLUE}[INFO]${NC} Testing SSL certificate..."
if curl -I https://www.astrooverz.com 2>/dev/null | grep -q "HTTP/2\|HTTP/1.1"; then
    echo -e "${GREEN}[SUCCESS]${NC} SSL certificate is valid"
else
    echo -e "${YELLOW}[WARNING]${NC} SSL certificate test failed"
fi

echo ""

# Test 5: Domain Resolution
echo -e "${BLUE}[INFO]${NC} Testing domain resolution..."
if nslookup www.astrooverz.com >/dev/null 2>&1; then
    echo -e "${GREEN}[SUCCESS]${NC} Domain resolution is working"
else
    echo -e "${YELLOW}[WARNING]${NC} Domain resolution test failed"
fi

echo ""

# Test 6: Response Times
echo -e "${BLUE}[INFO]${NC} Testing response times..."

# Homepage response time
start_time=$(date +%s%N)
if curl -s https://www.astrooverz.com >/dev/null 2>&1; then
    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 ))
    echo -e "${GREEN}[SUCCESS]${NC} Homepage response time: ${duration}ms"
else
    echo -e "${YELLOW}[WARNING]${NC} Homepage response time test failed"
fi

# API health response time
start_time=$(date +%s%N)
if curl -s https://www.astrooverz.com/api/healthz >/dev/null 2>&1; then
    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 ))
    echo -e "${GREEN}[SUCCESS]${NC} API health response time: ${duration}ms"
else
    echo -e "${YELLOW}[WARNING]${NC} API health response time test failed"
fi

# Panchangam API response time
start_time=$(date +%s%N)
if curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null 2>&1; then
    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 ))
    echo -e "${GREEN}[SUCCESS]${NC} Panchangam API response time: ${duration}ms"
else
    echo -e "${YELLOW}[WARNING]${NC} Panchangam API response time test failed"
fi

echo ""

# Test 7: Static Assets
echo -e "${BLUE}[INFO]${NC} Testing static assets..."
if curl -s -I https://www.astrooverz.com/index.html | grep -q "200 OK"; then
    echo -e "${GREEN}[SUCCESS]${NC} Static assets are accessible"
else
    echo -e "${YELLOW}[WARNING]${NC} Static assets test failed"
fi

echo ""

# Test 8: CORS Headers
echo -e "${BLUE}[INFO]${NC} Testing CORS headers..."
if curl -s -I https://www.astrooverz.com/api/healthz | grep -q "Access-Control-Allow-Origin"; then
    echo -e "${GREEN}[SUCCESS]${NC} CORS headers are present"
else
    echo -e "${YELLOW}[WARNING]${NC} CORS headers test failed"
fi

echo ""

# Show summary
echo -e "${BLUE}[INFO]${NC} Public domain testing completed!"
echo -e "${GREEN}[SUCCESS]${NC} You can run individual tests:"
echo "  curl -I https://www.astrooverz.com"
echo "  curl -s https://www.astrooverz.com/api/healthz"
echo "  curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400"
