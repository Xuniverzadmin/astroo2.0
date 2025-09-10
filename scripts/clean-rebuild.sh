#!/bin/bash

# Astrooverz Clean Rebuild and Restart Script
# This script performs a clean rebuild and restart of all services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VPS_IP="${VPS_IP:-}"
PROJECT_DIRS=("/opt/astrooverz" "/opt/astroo2.0" "/opt/astrooerz")

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

# Function to check if VPS_IP is set
check_vps_ip() {
    if [ -z "$VPS_IP" ]; then
        print_error "VPS_IP environment variable is not set"
        print_status "Please set VPS_IP before running this script:"
        print_status "export VPS_IP=your_vps_ip_address"
        exit 1
    fi
}

# Function to find the correct project directory
find_project_dir() {
    print_status "Finding the correct project directory..."
    
    for dir in "${PROJECT_DIRS[@]}"; do
        if ssh root@$VPS_IP "test -d $dir"; then
            print_success "Found project directory: $dir"
            echo "$dir"
            return 0
        fi
    done
    
    print_error "Could not find project directory in any of: ${PROJECT_DIRS[*]}"
    return 1
}

# Function to pull latest changes
pull_latest_changes() {
    local project_dir="$1"
    print_status "Pulling latest changes..."
    
    if ssh root@$VPS_IP "cd $project_dir && git pull --rebase"; then
        print_success "Latest changes pulled successfully"
        return 0
    else
        print_error "Failed to pull latest changes"
        return 1
    fi
}

# Function to stop all services
stop_services() {
    local project_dir="$1"
    print_status "Stopping all services..."
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose down"; then
        print_success "All services stopped successfully"
        return 0
    else
        print_error "Failed to stop services"
        return 1
    fi
}

# Function to build containers
build_containers() {
    local project_dir="$1"
    print_status "Building containers with no cache..."
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose build --no-cache"; then
        print_success "Containers built successfully"
        return 0
    else
        print_error "Failed to build containers"
        return 1
    fi
}

# Function to start services
start_services() {
    local project_dir="$1"
    print_status "Starting services..."
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose up -d --remove-orphans"; then
        print_success "Services started successfully"
        return 0
    else
        print_error "Failed to start services"
        return 1
    fi
}

# Function to check service status
check_service_status() {
    local project_dir="$1"
    print_status "Checking service status..."
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose ps"; then
        print_success "Service status checked"
        return 0
    else
        print_error "Failed to check service status"
        return 1
    fi
}

# Function to test endpoints
test_endpoints() {
    local project_dir="$1"
    print_status "Testing endpoints..."
    
    # Test backend health
    if ssh root@$VPS_IP "cd $project_dir && curl -s http://backend:8000/healthz"; then
        print_success "Backend health check passed"
    else
        print_warning "Backend health check failed"
    fi
    
    # Test API health
    if ssh root@$VPS_IP "cd $project_dir && curl -s http://backend:8000/api/healthz"; then
        print_success "API health check passed"
    else
        print_warning "API health check failed"
    fi
    
    # Test panchangam API
    if ssh root@$VPS_IP "cd $project_dir && curl -s 'http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400"; then
        print_success "Panchangam API test passed"
    else
        print_warning "Panchangam API test failed"
    fi
}

# Function to test public domain
test_public_domain() {
    print_status "Testing public domain..."
    
    # Test homepage
    if curl -I https://www.astrooverz.com >/dev/null 2>&1; then
        print_success "Homepage is accessible"
    else
        print_warning "Homepage test failed"
    fi
    
    # Test API health
    if curl -s https://www.astrooverz.com/api/healthz >/dev/null 2>&1; then
        print_success "API health endpoint is accessible"
    else
        print_warning "API health endpoint test failed"
    fi
    
    # Test panchangam API
    if curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null 2>&1; then
        print_success "Panchangam API is accessible"
    else
        print_warning "Panchangam API test failed"
    fi
}

# Function to perform clean rebuild
clean_rebuild() {
    print_status "Starting clean rebuild and restart..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Pull latest changes
    pull_latest_changes "$project_dir"
    echo ""
    
    # Stop all services
    stop_services "$project_dir"
    echo ""
    
    # Build containers
    build_containers "$project_dir"
    echo ""
    
    # Start services
    start_services "$project_dir"
    echo ""
    
    # Check service status
    check_service_status "$project_dir"
    echo ""
    
    # Test endpoints
    test_endpoints "$project_dir"
    echo ""
    
    # Test public domain
    test_public_domain
    echo ""
    
    echo "=========================================="
    print_status "Clean rebuild and restart completed!"
}

# Function to show help
show_help() {
    echo "Astrooverz Clean Rebuild and Restart Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  rebuild     - Perform clean rebuild and restart (default)"
    echo "  pull        - Pull latest changes only"
    echo "  stop        - Stop all services only"
    echo "  build       - Build containers only"
    echo "  start       - Start services only"
    echo "  status      - Check service status only"
    echo "  test        - Test endpoints only"
    echo "  help        - Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  VPS_IP      - VPS IP address (required)"
    echo ""
    echo "Examples:"
    echo "  export VPS_IP=192.168.1.100"
    echo "  $0 rebuild     # Perform clean rebuild and restart"
    echo "  $0 pull        # Pull latest changes only"
    echo "  $0 status      # Check service status only"
}

# Function to show service status
show_service_status() {
    print_status "Showing service status..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Check service status
    check_service_status "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Service status completed!"
}

# Function to pull changes only
pull_changes_only() {
    print_status "Pulling latest changes..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Pull latest changes
    pull_latest_changes "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Pull changes completed!"
}

# Function to stop services only
stop_services_only() {
    print_status "Stopping all services..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Stop all services
    stop_services "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Stop services completed!"
}

# Function to build containers only
build_containers_only() {
    print_status "Building containers..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Build containers
    build_containers "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Build containers completed!"
}

# Function to start services only
start_services_only() {
    print_status "Starting services..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Start services
    start_services "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Start services completed!"
}

# Function to test endpoints only
test_endpoints_only() {
    print_status "Testing endpoints..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Test endpoints
    test_endpoints "$project_dir"
    echo ""
    
    # Test public domain
    test_public_domain
    echo ""
    
    echo "=========================================="
    print_status "Endpoint testing completed!"
}

# Main script logic
main() {
    case "${1:-rebuild}" in
        rebuild)
            clean_rebuild
            ;;
        pull)
            pull_changes_only
            ;;
        stop)
            stop_services_only
            ;;
        build)
            build_containers_only
            ;;
        start)
            start_services_only
            ;;
        status)
            show_service_status
            ;;
        test)
            test_endpoints_only
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
