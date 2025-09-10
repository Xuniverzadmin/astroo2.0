#!/bin/bash

# Astrooverz Frontend Testing Script
# This script tests the frontend serving through Caddy

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FRONTEND_URL="http://frontend:80"
CADDY_URL="http://caddy:80"
LOCAL_URL="http://localhost:80"

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

# Function to test frontend through Caddy (exact command as requested)
test_frontend_through_caddy() {
    print_status "Testing frontend through Caddy (exact command as requested)..."
    
    if response=$(docker compose exec caddy sh -lc 'wget -qO- http://frontend:80 | head -n 20' 2>/dev/null); then
        print_success "Frontend is serving through Caddy"
        echo "Response (first 20 lines):"
        echo "$response"
        return 0
    else
        print_error "Frontend test through Caddy failed"
        return 1
    fi
}

# Function to test frontend directly
test_frontend_direct() {
    print_status "Testing frontend service directly..."
    
    if response=$(docker compose exec frontend sh -c 'wget -qO- http://localhost:5173 | head -n 20' 2>/dev/null); then
        print_success "Frontend service is working directly"
        echo "Response (first 20 lines):"
        echo "$response"
        return 0
    else
        print_error "Frontend service test failed"
        return 1
    fi
}

# Function to test Caddy serving
test_caddy_serving() {
    print_status "Testing Caddy serving frontend..."
    
    if response=$(docker compose exec caddy sh -c 'wget -qO- http://localhost:80 | head -n 20' 2>/dev/null); then
        print_success "Caddy is serving frontend"
        echo "Response (first 20 lines):"
        echo "$response"
        return 0
    else
        print_error "Caddy serving test failed"
        return 1
    fi
}

# Function to test external access
test_external_access() {
    print_status "Testing external access to frontend..."
    
    if response=$(curl -s http://localhost:80 | head -n 20 2>/dev/null); then
        print_success "External access to frontend is working"
        echo "Response (first 20 lines):"
        echo "$response"
        return 0
    else
        print_error "External access to frontend failed"
        return 1
    fi
}

# Function to test frontend health
test_frontend_health() {
    print_status "Testing frontend health endpoint..."
    
    if response=$(curl -s http://localhost:5173 2>/dev/null); then
        print_success "Frontend health check passed"
        echo "Response (first 10 lines):"
        echo "$response" | head -n 10
        return 0
    else
        print_error "Frontend health check failed"
        return 1
    fi
}

# Function to test static assets
test_static_assets() {
    print_status "Testing static assets..."
    
    local assets=("index.html" "styles.css" "main.js")
    local success_count=0
    local total_count=${#assets[@]}
    
    for asset in "${assets[@]}"; do
        if curl -s -I http://localhost:80/$asset | grep -q "200 OK"; then
            print_success "Asset $asset is accessible"
            ((success_count++))
        else
            print_warning "Asset $asset is not accessible"
        fi
    done
    
    if [ $success_count -eq $total_count ]; then
        print_success "All static assets are accessible"
        return 0
    else
        print_warning "$success_count/$total_count static assets are accessible"
        return 1
    fi
}

# Function to test API proxy through Caddy
test_api_proxy() {
    print_status "Testing API proxy through Caddy..."
    
    if response=$(curl -s http://localhost:80/api/healthz 2>/dev/null); then
        print_success "API proxy through Caddy is working"
        echo "Response: $response"
        return 0
    else
        print_error "API proxy through Caddy failed"
        return 1
    fi
}

# Function to test Caddy configuration
test_caddy_config() {
    print_status "Testing Caddy configuration..."
    
    if docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile 2>/dev/null; then
        print_success "Caddy configuration is valid"
        return 0
    else
        print_error "Caddy configuration is invalid"
        return 1
    fi
}

# Function to test all frontend endpoints
test_all_frontend() {
    print_status "Testing all frontend endpoints..."
    echo "=========================================="
    
    local total_tests=0
    local passed_tests=0
    
    # Test frontend through Caddy (exact command)
    ((total_tests++))
    if test_frontend_through_caddy; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test frontend directly
    ((total_tests++))
    if test_frontend_direct; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test Caddy serving
    ((total_tests++))
    if test_caddy_serving; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test external access
    ((total_tests++))
    if test_external_access; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test frontend health
    ((total_tests++))
    if test_frontend_health; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test static assets
    ((total_tests++))
    if test_static_assets; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test API proxy
    ((total_tests++))
    if test_api_proxy; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test Caddy configuration
    ((total_tests++))
    if test_caddy_config; then
        ((passed_tests++))
    fi
    echo ""
    
    echo "=========================================="
    print_status "Frontend Test Summary: $passed_tests/$total_tests tests passed"
    
    if [ $passed_tests -eq $total_tests ]; then
        print_success "All frontend tests passed!"
        return 0
    else
        print_warning "Some frontend tests failed"
        return 1
    fi
}

# Function to show help
show_help() {
    echo "Astrooverz Frontend Testing Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  test        - Test all frontend endpoints (default)"
    echo "  caddy       - Test frontend through Caddy (exact command)"
    echo "  direct      - Test frontend service directly"
    echo "  external    - Test external access"
    echo "  assets      - Test static assets"
    echo "  api-proxy   - Test API proxy through Caddy"
    echo "  config      - Test Caddy configuration"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 test        # Test all frontend endpoints"
    echo "  $0 caddy       # Test frontend through Caddy"
    echo "  $0 external    # Test external access"
    echo "  $0 assets      # Test static assets"
}

# Function to show service status
show_status() {
    print_status "Frontend service status:"
    
    echo "=== Docker Compose Status ==="
    docker compose ps frontend caddy
    
    echo ""
    echo "=== Frontend Logs (last 10 lines) ==="
    docker compose logs --tail=10 frontend
    
    echo ""
    echo "=== Caddy Logs (last 10 lines) ==="
    docker compose logs --tail=10 caddy
    
    echo ""
    echo "=== Network Connectivity ==="
    docker compose exec frontend sh -c 'curl -s -I http://localhost:5173 | head -1' 2>/dev/null || echo "Frontend not accessible"
    docker compose exec caddy sh -c 'curl -s -I http://localhost:80 | head -1' 2>/dev/null || echo "Caddy not accessible"
}

# Main script logic
main() {
    case "${1:-test}" in
        test)
            test_all_frontend
            ;;
        caddy)
            test_frontend_through_caddy
            ;;
        direct)
            test_frontend_direct
            ;;
        external)
            test_external_access
            ;;
        assets)
            test_static_assets
            ;;
        api-proxy)
            test_api_proxy
            ;;
        config)
            test_caddy_config
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
