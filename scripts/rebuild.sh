#!/bin/bash

# Astrooverz Container Rebuild Script
# This script safely rebuilds and restarts containers with new code

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/opt/astrooverz"
LOG_FILE="/var/log/astrooverz-rebuild.log"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root"
        exit 1
    fi
}

# Function to setup logging
setup_logging() {
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"
    print_status "Logging to: $LOG_FILE"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker >/dev/null 2>&1; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose >/dev/null 2>&1; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    if [ ! -d "$PROJECT_DIR" ]; then
        print_error "Project directory not found: $PROJECT_DIR"
        exit 1
    fi
    
    cd "$PROJECT_DIR"
    
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found in $PROJECT_DIR"
        exit 1
    fi
    
    print_success "All prerequisites are met"
}

# Function to backup database before rebuild
backup_database() {
    print_status "Creating database backup before rebuild..."
    
    cd "$PROJECT_DIR"
    
    # Create backup directory
    mkdir -p backups
    
    # Create backup
    local backup_file="backups/astrooverz_pre_rebuild_$(date +%Y%m%d_%H%M%S).sql"
    
    if docker-compose exec -T db pg_dump -U astrooverz astrooverz > "$backup_file" 2>/dev/null; then
        print_success "Database backup created: $backup_file"
    else
        print_warning "Could not create database backup (database might not be running)"
    fi
}

# Function to pull latest images
pull_images() {
    print_status "Pulling latest images from registry..."
    
    cd "$PROJECT_DIR"
    
    # Try to pull images (safe to run even if no registry)
    if docker-compose pull; then
        print_success "Images pulled successfully"
    else
        print_warning "Could not pull images (no registry or network issue)"
    fi
}

# Function to stop services gracefully
stop_services() {
    print_status "Stopping services gracefully..."
    
    cd "$PROJECT_DIR"
    
    # Stop services with timeout
    docker-compose down --timeout 30
    
    print_success "Services stopped"
}

# Function to clean up old containers and images
cleanup_old() {
    print_status "Cleaning up old containers and images..."
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove unused images (keep recent ones)
    docker image prune -f
    
    # Remove unused networks
    docker network prune -f
    
    print_success "Cleanup completed"
}

# Function to rebuild containers
rebuild_containers() {
    print_status "Rebuilding containers with new code..."
    
    cd "$PROJECT_DIR"
    
    # Force rebuild without cache
    docker-compose build --no-cache --pull
    
    print_success "Containers rebuilt successfully"
}

# Function to start services
start_services() {
    print_status "Starting services..."
    
    cd "$PROJECT_DIR"
    
    # Start services with orphan removal
    docker-compose up -d --remove-orphans
    
    print_success "Services started"
}

# Function to wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to be healthy..."
    
    local max_attempts=60  # 10 minutes total
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        # Check if any service is healthy
        if docker-compose ps | grep -q "healthy"; then
            print_success "Services are healthy"
            return 0
        fi
        
        # Check if services are at least running
        if docker-compose ps | grep -q "Up"; then
            print_status "Services are running, waiting for health checks..."
        else
            print_status "Waiting for services to start..."
        fi
        
        sleep 10
        ((attempt++))
    done
    
    print_warning "Services may not be fully healthy yet"
    return 1
}

# Function to verify deployment
verify_deployment() {
    print_status "Verifying deployment..."
    
    local errors=0
    
    # Wait a bit more for services to be fully ready
    sleep 30
    
    # Check backend health
    if curl -f http://localhost:8000/healthz >/dev/null 2>&1; then
        print_success "Backend health check passed"
    else
        print_error "Backend health check failed"
        ((errors++))
    fi
    
    # Check API health
    if curl -f http://localhost:8000/api/healthz >/dev/null 2>&1; then
        print_success "API health check passed"
    else
        print_error "API health check failed"
        ((errors++))
    fi
    
    # Check frontend
    if curl -f http://localhost:5173 >/dev/null 2>&1; then
        print_success "Frontend health check passed"
    else
        print_error "Frontend health check failed"
        ((errors++))
    fi
    
    # Test panchangam API
    if curl -f "http://localhost:8000/api/panchangam/2024-03-15?lat=13.0827&lon=80.2707&tz=Asia/Kolkata" >/dev/null 2>&1; then
        print_success "Panchangam API test passed"
    else
        print_error "Panchangam API test failed"
        ((errors++))
    fi
    
    if [ $errors -eq 0 ]; then
        print_success "All health checks passed"
        return 0
    else
        print_error "$errors health check(s) failed"
        return 1
    fi
}

# Function to show service status
show_status() {
    print_status "Service status:"
    
    cd "$PROJECT_DIR"
    
    echo "=== Docker Compose Status ==="
    docker-compose ps
    
    echo ""
    echo "=== Resource Usage ==="
    docker stats --no-stream
    
    echo ""
    echo "=== Recent Logs ==="
    docker-compose logs --tail=20
}

# Function to rollback if needed
rollback() {
    print_error "Deployment failed, attempting rollback..."
    
    cd "$PROJECT_DIR"
    
    # Stop current services
    docker-compose down
    
    # Try to restore from backup if available
    local latest_backup=$(ls -t backups/astrooverz_pre_rebuild_*.sql 2>/dev/null | head -1)
    if [ -n "$latest_backup" ]; then
        print_status "Restoring from backup: $latest_backup"
        docker-compose up -d db
        sleep 30
        docker-compose exec -T db psql -U astrooverz -d astrooverz < "$latest_backup"
        docker-compose up -d
    else
        print_warning "No backup found for rollback"
    fi
}

# Function to show help
show_help() {
    echo "Astrooverz Container Rebuild Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  rebuild     - Full rebuild (backup, pull, build, restart)"
    echo "  quick       - Quick rebuild (no backup, no pull)"
    echo "  pull        - Pull images only"
    echo "  build       - Build containers only"
    echo "  restart     - Restart services only"
    echo "  status      - Show service status"
    echo "  logs        - Show service logs"
    echo "  cleanup     - Clean up old containers and images"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 rebuild     # Full rebuild with backup"
    echo "  $0 quick       # Quick rebuild without backup"
    echo "  $0 status      # Check status"
    echo "  $0 logs        # View logs"
}

# Function to show logs
show_logs() {
    print_status "Showing service logs..."
    
    cd "$PROJECT_DIR"
    
    docker-compose logs -f --tail=100
}

# Main rebuild function
full_rebuild() {
    print_status "Starting full rebuild process..."
    
    check_prerequisites
    backup_database
    pull_images
    stop_services
    cleanup_old
    rebuild_containers
    start_services
    wait_for_services
    
    if verify_deployment; then
        print_success "Full rebuild completed successfully!"
        show_status
    else
        print_error "Deployment verification failed"
        rollback
        exit 1
    fi
}

# Quick rebuild function (no backup, no pull)
quick_rebuild() {
    print_status "Starting quick rebuild process..."
    
    check_prerequisites
    stop_services
    cleanup_old
    rebuild_containers
    start_services
    wait_for_services
    
    if verify_deployment; then
        print_success "Quick rebuild completed successfully!"
        show_status
    else
        print_error "Deployment verification failed"
        rollback
        exit 1
    fi
}

# Pull only function
pull_only() {
    print_status "Pulling latest images..."
    
    check_prerequisites
    pull_images
    print_success "Images pulled successfully"
}

# Build only function
build_only() {
    print_status "Building containers..."
    
    check_prerequisites
    rebuild_containers
    print_success "Containers built successfully"
}

# Restart only function
restart_only() {
    print_status "Restarting services..."
    
    check_prerequisites
    stop_services
    start_services
    wait_for_services
    
    if verify_deployment; then
        print_success "Services restarted successfully!"
        show_status
    else
        print_error "Service restart verification failed"
        exit 1
    fi
}

# Main script logic
main() {
    case "${1:-help}" in
        rebuild)
            check_root
            setup_logging
            full_rebuild
            ;;
        quick)
            check_root
            setup_logging
            quick_rebuild
            ;;
        pull)
            check_root
            setup_logging
            pull_only
            ;;
        build)
            check_root
            setup_logging
            build_only
            ;;
        restart)
            check_root
            setup_logging
            restart_only
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        cleanup)
            check_root
            setup_logging
            cleanup_old
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
