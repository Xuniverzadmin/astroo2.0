#!/bin/bash

# Astrooverz Debug and Deploy Script
# This script helps debug and deploy the new build

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

# Function to check git status
check_git_status() {
    local project_dir="$1"
    print_status "Checking git status in $project_dir..."
    
    if ssh root@$VPS_IP "cd $project_dir && git status"; then
        print_success "Git status checked successfully"
        return 0
    else
        print_error "Failed to check git status"
        return 1
    fi
}

# Function to fetch latest changes
fetch_latest_changes() {
    local project_dir="$1"
    print_status "Fetching latest changes from remote..."
    
    if ssh root@$VPS_IP "cd $project_dir && git fetch --all"; then
        print_success "Latest changes fetched successfully"
        return 0
    else
        print_error "Failed to fetch latest changes"
        return 1
    fi
}

# Function to get current commit hash
get_current_commit() {
    local project_dir="$1"
    print_status "Getting current commit hash..."
    
    if commit_hash=$(ssh root@$VPS_IP "cd $project_dir && git rev-parse --short HEAD"); then
        print_success "Current commit hash: $commit_hash"
        echo "$commit_hash"
        return 0
    else
        print_error "Failed to get current commit hash"
        return 1
    fi
}

# Function to check if commit matches local
check_commit_match() {
    local project_dir="$1"
    local local_commit="$2"
    
    print_status "Checking if commit matches local..."
    
    if remote_commit=$(ssh root@$VPS_IP "cd $project_dir && git rev-parse --short HEAD"); then
        if [ "$remote_commit" = "$local_commit" ]; then
            print_success "Commit hash matches local: $remote_commit"
            return 0
        else
            print_warning "Commit hash mismatch:"
            print_warning "  Local:  $local_commit"
            print_warning "  Remote: $remote_commit"
            return 1
        fi
    else
        print_error "Failed to get remote commit hash"
        return 1
    fi
}

# Function to get local commit hash
get_local_commit() {
    print_status "Getting local commit hash..."
    
    if local_commit=$(git rev-parse --short HEAD); then
        print_success "Local commit hash: $local_commit"
        echo "$local_commit"
        return 0
    else
        print_error "Failed to get local commit hash"
        return 1
    fi
}

# Function to check out main branch
checkout_main() {
    local project_dir="$1"
    print_status "Checking out main branch..."
    
    if ssh root@$VPS_IP "cd $project_dir && git checkout main"; then
        print_success "Switched to main branch"
        return 0
    else
        print_error "Failed to switch to main branch"
        return 1
    fi
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

# Function to check environment file
check_env_file() {
    local project_dir="$1"
    print_status "Checking environment file..."
    
    if ssh root@$VPS_IP "cd $project_dir && ls -la .env .env.sample"; then
        print_success "Environment files found"
        return 0
    else
        print_warning "Environment files not found or not accessible"
        return 1
    fi
}

# Function to show environment file contents
show_env_contents() {
    local project_dir="$1"
    print_status "Showing environment file contents..."
    
    if ssh root@$VPS_IP "cd $project_dir && cat .env"; then
        print_success "Environment file contents displayed"
        return 0
    else
        print_error "Failed to display environment file contents"
        return 1
    fi
}

# Function to check Docker services
check_docker_services() {
    local project_dir="$1"
    print_status "Checking Docker services..."
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose ps"; then
        print_success "Docker services status checked"
        return 0
    else
        print_error "Failed to check Docker services"
        return 1
    fi
}

# Function to check Docker logs
check_docker_logs() {
    local project_dir="$1"
    print_status "Checking Docker logs..."
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose logs --tail=20"; then
        print_success "Docker logs checked"
        return 0
    else
        print_error "Failed to check Docker logs"
        return 1
    fi
}

# Function to rebuild containers
rebuild_containers() {
    local project_dir="$1"
    print_status "Rebuilding containers..."
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose pull || true"; then
        print_success "Docker images pulled"
    else
        print_warning "Failed to pull Docker images"
    fi
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose build --no-cache"; then
        print_success "Containers rebuilt successfully"
    else
        print_error "Failed to rebuild containers"
        return 1
    fi
    
    if ssh root@$VPS_IP "cd $project_dir && docker compose up -d --remove-orphans"; then
        print_success "Containers started successfully"
        return 0
    else
        print_error "Failed to start containers"
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

# Function to show help
show_help() {
    echo "Astrooverz Debug and Deploy Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  debug       - Debug current deployment (default)"
    echo "  deploy      - Deploy new build"
    echo "  status      - Show deployment status"
    echo "  logs        - Show Docker logs"
    echo "  test        - Test endpoints"
    echo "  public      - Test public domain"
    echo "  help        - Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  VPS_IP      - VPS IP address (required)"
    echo ""
    echo "Examples:"
    echo "  export VPS_IP=192.168.1.100"
    echo "  $0 debug        # Debug current deployment"
    echo "  $0 deploy       # Deploy new build"
    echo "  $0 status       # Show deployment status"
    echo "  $0 test         # Test endpoints"
    echo "  $0 public       # Test public domain"
}

# Function to debug deployment
debug_deployment() {
    print_status "Starting deployment debug..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Get local commit hash
    if ! local_commit=$(get_local_commit); then
        exit 1
    fi
    
    # Check git status
    check_git_status "$project_dir"
    echo ""
    
    # Fetch latest changes
    fetch_latest_changes "$project_dir"
    echo ""
    
    # Get current commit hash
    if ! current_commit=$(get_current_commit "$project_dir"); then
        exit 1
    fi
    echo ""
    
    # Check if commit matches local
    check_commit_match "$project_dir" "$local_commit"
    echo ""
    
    # Check environment file
    check_env_file "$project_dir"
    echo ""
    
    # Show environment file contents
    show_env_contents "$project_dir"
    echo ""
    
    # Check Docker services
    check_docker_services "$project_dir"
    echo ""
    
    # Check Docker logs
    check_docker_logs "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Debug completed!"
}

# Function to deploy new build
deploy_new_build() {
    print_status "Starting new build deployment..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Get local commit hash
    if ! local_commit=$(get_local_commit); then
        exit 1
    fi
    
    # Check out main branch
    checkout_main "$project_dir"
    echo ""
    
    # Pull latest changes
    pull_latest_changes "$project_dir"
    echo ""
    
    # Check if commit matches local
    check_commit_match "$project_dir" "$local_commit"
    echo ""
    
    # Check environment file
    check_env_file "$project_dir"
    echo ""
    
    # Rebuild containers
    rebuild_containers "$project_dir"
    echo ""
    
    # Test endpoints
    test_endpoints "$project_dir"
    echo ""
    
    # Test public domain
    test_public_domain
    echo ""
    
    echo "=========================================="
    print_status "New build deployment completed!"
}

# Function to show deployment status
show_deployment_status() {
    print_status "Showing deployment status..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Check git status
    check_git_status "$project_dir"
    echo ""
    
    # Get current commit hash
    get_current_commit "$project_dir"
    echo ""
    
    # Check Docker services
    check_docker_services "$project_dir"
    echo ""
    
    # Test endpoints
    test_endpoints "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Deployment status completed!"
}

# Function to show Docker logs
show_docker_logs() {
    print_status "Showing Docker logs..."
    echo "=========================================="
    
    # Check VPS IP
    check_vps_ip
    
    # Find project directory
    if ! project_dir=$(find_project_dir); then
        exit 1
    fi
    
    # Check Docker logs
    check_docker_logs "$project_dir"
    echo ""
    
    echo "=========================================="
    print_status "Docker logs completed!"
}

# Function to test endpoints
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
    
    echo "=========================================="
    print_status "Endpoint testing completed!"
}

# Function to test public domain
test_public_domain_only() {
    print_status "Testing public domain..."
    echo "=========================================="
    
    # Test public domain
    test_public_domain
    echo ""
    
    echo "=========================================="
    print_status "Public domain testing completed!"
}

# Main script logic
main() {
    case "${1:-debug}" in
        debug)
            debug_deployment
            ;;
        deploy)
            deploy_new_build
            ;;
        status)
            show_deployment_status
            ;;
        logs)
            show_docker_logs
            ;;
        test)
            test_endpoints_only
            ;;
        public)
            test_public_domain_only
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
