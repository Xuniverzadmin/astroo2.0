#!/bin/bash

# Astrooverz VPS Deployment Script
# This script automates the deployment process on your VPS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/opt/astrooverz"
BACKUP_DIR="/opt/astrooverz/backups"
LOG_FILE="/var/log/astrooverz-deploy.log"

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

# Function to create log directory
setup_logging() {
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"
    print_status "Logging to: $LOG_FILE"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command -v docker >/dev/null 2>&1; then
        missing_deps+=("docker")
    fi
    
    if ! command -v docker-compose >/dev/null 2>&1; then
        missing_deps+=("docker-compose")
    fi
    
    if ! command -v git >/dev/null 2>&1; then
        missing_deps+=("git")
    fi
    
    if ! command -v curl >/dev/null 2>&1; then
        missing_deps+=("curl")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_error "Please install the missing dependencies and try again."
        exit 1
    fi
    
    print_success "All prerequisites are installed"
}

# Function to setup project directory
setup_project_directory() {
    print_status "Setting up project directory..."
    
    if [ ! -d "$PROJECT_DIR" ]; then
        mkdir -p "$PROJECT_DIR"
        print_status "Created project directory: $PROJECT_DIR"
    fi
    
    cd "$PROJECT_DIR"
    
    # Clone repository if it doesn't exist
    if [ ! -d ".git" ]; then
        print_status "Cloning repository..."
        git clone https://github.com/YOUR_USERNAME/astro2.0.git .
        print_success "Repository cloned"
    else
        print_status "Repository already exists, updating..."
    fi
}

# Function to update code
update_code() {
    print_status "Updating code from repository..."
    
    cd "$PROJECT_DIR"
    
    # Fetch all branches and tags
    git fetch --all
    
    # Checkout main branch
    git checkout main
    
    # Pull latest changes
    git pull --rebase
    
    print_success "Code updated successfully"
}

# Function to setup environment
setup_environment() {
    print_status "Setting up environment configuration..."
    
    cd "$PROJECT_DIR"
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        if [ -f "env.sample" ]; then
            print_status "Creating .env from template..."
            cp env.sample .env
            print_warning "Please edit .env file with your configuration"
            print_warning "Run: nano .env"
        else
            print_error ".env file not found and no template available"
            exit 1
        fi
    else
        print_status ".env file already exists"
    fi
    
    # Display current environment configuration
    print_status "Current environment configuration:"
    echo "----------------------------------------"
    cat .env | grep -v "^#" | grep -v "^$" | head -10
    echo "----------------------------------------"
}

# Function to create production docker-compose override
create_production_compose() {
    print_status "Creating production docker-compose configuration..."
    
    cd "$PROJECT_DIR"
    
    cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  backend:
    restart: unless-stopped
    environment:
      - SCHED_ENABLED=true
      - CITY_PRECOMPUTE=IN_TOP200
      - PRECOMPUTE_DAYS=30
      - PRECOMPUTE_TIME=02:30
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5173"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  caddy:
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - caddy_data:/data
      - caddy_config:/config
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:2019/config/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    restart: unless-stopped
    environment:
      - POSTGRES_DB=astrooverz
      - POSTGRES_USER=astrooverz
      - POSTGRES_PASSWORD=astrooverz123
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U astrooverz -d astrooverz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  pgdata:
  redisdata:
  caddy_data:
  caddy_config:

networks:
  web:
    driver: bridge
EOF
    
    print_success "Production docker-compose configuration created"
}

# Function to backup database
backup_database() {
    print_status "Creating database backup..."
    
    cd "$PROJECT_DIR"
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    
    # Create backup
    local backup_file="$BACKUP_DIR/astrooverz_$(date +%Y%m%d_%H%M%S).sql"
    
    if docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec -T db pg_dump -U astrooverz astrooverz > "$backup_file" 2>/dev/null; then
        print_success "Database backup created: $backup_file"
    else
        print_warning "Could not create database backup (database might not be running)"
    fi
    
    # Clean up old backups (keep last 7 days)
    find "$BACKUP_DIR" -name "astrooverz_*.sql" -mtime +7 -delete 2>/dev/null || true
}

# Function to pull latest images
pull_images() {
    print_status "Pulling latest Docker images..."
    
    cd "$PROJECT_DIR"
    
    # Login to GitHub Container Registry if needed
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin
    fi
    
    # Pull images
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml pull
    
    print_success "Docker images pulled successfully"
}

# Function to stop services
stop_services() {
    print_status "Stopping existing services..."
    
    cd "$PROJECT_DIR"
    
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down --remove-orphans
    
    print_success "Services stopped"
}

# Function to start services
start_services() {
    print_status "Starting services..."
    
    cd "$PROJECT_DIR"
    
    # Start services
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
    
    print_success "Services started"
}

# Function to wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to be healthy..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps | grep -q "healthy"; then
            print_success "Services are healthy"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - waiting for services..."
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
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps
    
    echo ""
    echo "=== Resource Usage ==="
    docker stats --no-stream
    
    echo ""
    echo "=== Disk Usage ==="
    df -h
    
    echo ""
    echo "=== Memory Usage ==="
    free -h
}

# Function to cleanup old images
cleanup_images() {
    print_status "Cleaning up old Docker images..."
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused containers
    docker container prune -f
    
    # Remove unused volumes (be careful with this)
    # docker volume prune -f
    
    print_success "Cleanup completed"
}

# Function to rebuild containers
rebuild_containers() {
    print_status "Rebuilding containers with new code..."
    
    cd "$PROJECT_DIR"
    
    # Pull latest images (safe to run)
    docker-compose pull || true
    
    # Force rebuild without cache
    docker-compose build --no-cache
    
    # Start services with orphan removal
    docker-compose up -d --remove-orphans
    
    print_success "Containers rebuilt and restarted"
}

# Function to show help
show_help() {
    echo "Astrooverz VPS Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy     - Full deployment (backup, update, deploy)"
    echo "  update     - Update code and redeploy"
    echo "  rebuild    - Rebuild containers with new code"
    echo "  restart    - Restart services"
    echo "  stop       - Stop services"
    echo "  start      - Start services"
    echo "  status     - Show service status"
    echo "  backup     - Create database backup"
    echo "  cleanup    - Clean up old images"
    echo "  verify     - Verify deployment health"
    echo "  logs       - Show service logs"
    echo "  help       - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy     # Full deployment"
    echo "  $0 update     # Quick update"
    echo "  $0 rebuild    # Rebuild containers"
    echo "  $0 status     # Check status"
    echo "  $0 logs       # View logs"
}

# Function to show logs
show_logs() {
    print_status "Showing service logs..."
    
    cd "$PROJECT_DIR"
    
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f --tail=100
}

# Main deployment function
full_deploy() {
    print_status "Starting full deployment..."
    
    check_prerequisites
    setup_project_directory
    update_code
    setup_environment
    create_production_compose
    backup_database
    pull_images
    stop_services
    start_services
    wait_for_services
    verify_deployment
    cleanup_images
    
    print_success "Full deployment completed successfully!"
    show_status
}

# Quick update function
quick_update() {
    print_status "Starting quick update..."
    
    update_code
    pull_images
    stop_services
    start_services
    wait_for_services
    verify_deployment
    
    print_success "Quick update completed successfully!"
}

# Main script logic
main() {
    case "${1:-help}" in
        deploy)
            check_root
            setup_logging
            full_deploy
            ;;
        update)
            check_root
            setup_logging
            quick_update
            ;;
        rebuild)
            check_root
            setup_logging
            rebuild_containers
            wait_for_services
            verify_deployment
            ;;
        restart)
            check_root
            setup_logging
            stop_services
            start_services
            wait_for_services
            verify_deployment
            ;;
        stop)
            check_root
            setup_logging
            stop_services
            ;;
        start)
            check_root
            setup_logging
            start_services
            wait_for_services
            verify_deployment
            ;;
        status)
            show_status
            ;;
        backup)
            check_root
            setup_logging
            backup_database
            ;;
        cleanup)
            check_root
            setup_logging
            cleanup_images
            ;;
        verify)
            verify_deployment
            ;;
        logs)
            show_logs
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
