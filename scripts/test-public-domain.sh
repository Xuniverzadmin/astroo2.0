#!/bin/bash

# Astrooverz Public Domain Testing Script
# This script tests the public domain endpoints

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="https://www.astrooverz.com"
API_BASE="$DOMAIN/api"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to test public domain homepage
test_homepage() {
    print_status "Testing public domain homepage..."
    
    if response=$(curl -I "$DOMAIN" 2>/dev/null); then
        print_success "Homepage is accessible"
        echo "Response headers:"
        echo "$response"
        return 0
    else
        print_error "Homepage test failed"
        return 1
    fi
}

# Function to test API health endpoint
test_api_health() {
    print_status "Testing API health endpoint..."
    
    if response=$(curl -s "$API_BASE/healthz" 2>/dev/null); then
        print_success "API health endpoint is working"
        echo "Response: $response"
        return 0
    else
        print_error "API health endpoint test failed"
        return 1
    fi
}

# Function to test panchangam API
test_panchangam_api() {
    print_status "Testing panchangam API..."
    
    local url="$API_BASE/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata"
    
    if response=$(curl -s "$url" 2>/dev/null); then
        print_success "Panchangam API is working"
        echo "Response (first 400 characters):"
        echo "$response" | head -c 400
        echo ""
        return 0
    else
        print_error "Panchangam API test failed"
        return 1
    fi
}

# Function to test SSL certificate
test_ssl_certificate() {
    print_status "Testing SSL certificate..."
    
    if response=$(curl -I "$DOMAIN" 2>/dev/null | grep -i "HTTP/2\|HTTP/1.1"); then
        print_success "SSL certificate is valid"
        echo "HTTP response: $response"
        return 0
    else
        print_error "SSL certificate test failed"
        return 1
    fi
}

# Function to test domain resolution
test_domain_resolution() {
    print_status "Testing domain resolution..."
    
    if response=$(nslookup www.astrooverz.com 2>/dev/null | grep -A 1 "Name:"); then
        print_success "Domain resolution is working"
        echo "DNS response:"
        echo "$response"
        return 0
    else
        print_error "Domain resolution test failed"
        return 1
    fi
}

# Function to test response times
test_response_times() {
    print_status "Testing response times..."
    
    local endpoints=("$DOMAIN" "$API_BASE/healthz" "$API_BASE/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata")
    
    for endpoint in "${endpoints[@]}"; do
        local start_time=$(date +%s%N)
        if curl -s "$endpoint" >/dev/null 2>&1; then
            local end_time=$(date +%s%N)
            local duration=$(( (end_time - start_time) / 1000000 ))
            print_success "Response time for $endpoint: ${duration}ms"
        else
            print_error "Failed to get response time for $endpoint"
        fi
    done
}

# Function to test all endpoints
test_all_endpoints() {
    print_status "Testing all public domain endpoints..."
    echo "=========================================="
    
    local total_tests=0
    local passed_tests=0
    
    # Test homepage
    ((total_tests++))
    if test_homepage; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test API health
    ((total_tests++))
    if test_api_health; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test panchangam API
    ((total_tests++))
    if test_panchangam_api; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test SSL certificate
    ((total_tests++))
    if test_ssl_certificate; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test domain resolution
    ((total_tests++))
    if test_domain_resolution; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test response times
    ((total_tests++))
    if test_response_times; then
        ((passed_tests++))
    fi
    echo ""
    
    echo "=========================================="
    print_status "Public Domain Test Summary: $passed_tests/$total_tests tests passed"
    
    if [ $passed_tests -eq $total_tests ]; then
        print_success "All public domain tests passed!"
        return 0
    else
        print_warning "Some public domain tests failed"
        return 1
    fi
}

# Function to show help
show_help() {
    echo "Astrooverz Public Domain Testing Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  test        - Test all public domain endpoints (default)"
    echo "  homepage    - Test homepage"
    echo "  health      - Test API health endpoint"
    echo "  panchangam  - Test panchangam API"
    echo "  ssl         - Test SSL certificate"
    echo "  dns         - Test domain resolution"
    echo "  performance - Test response times"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 test        # Test all endpoints"
    echo "  $0 homepage    # Test homepage only"
    echo "  $0 health      # Test API health only"
    echo "  $0 panchangam  # Test panchangam API only"
}

# Function to show service status
show_status() {
    print_status "Public domain service status:"
    
    echo "=== Domain Resolution ==="
    nslookup www.astrooverz.com 2>/dev/null || echo "DNS resolution failed"
    
    echo ""
    echo "=== SSL Certificate ==="
    curl -I "$DOMAIN" 2>/dev/null | head -1 || echo "SSL test failed"
    
    echo ""
    echo "=== Homepage Status ==="
    curl -s -I "$DOMAIN" 2>/dev/null | head -1 || echo "Homepage test failed"
    
    echo ""
    echo "=== API Status ==="
    curl -s "$API_BASE/healthz" 2>/dev/null || echo "API test failed"
}

# Main script logic
main() {
    case "${1:-test}" in
        test)
            test_all_endpoints
            ;;
        homepage)
            test_homepage
            ;;
        health)
            test_api_health
            ;;
        panchangam)
            test_panchangam_api
            ;;
        ssl)
            test_ssl_certificate
            ;;
        dns)
            test_domain_resolution
            ;;
        performance)
            test_response_times
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
