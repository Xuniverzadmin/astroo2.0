#!/bin/bash

# VPS Deployment Script for Astrooverz.com
# This script deploys the latest code to VPS and updates the website

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VPS_IP="${VPS_IP:-}"
PROJECT_DIR="${PROJECT_DIR:-/opt/astrooverz}"
BACKUP_DIR="${BACKUP_DIR:-/opt/backups}"

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

check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if [ -z "$VPS_IP" ]; then
        print_error "VPS_IP environment variable not set"
        print_status "Please set VPS_IP environment variable"
        print_status "Example: VPS_IP=your.vps.ip ./deploy-to-vps.sh"
        exit 1
    fi
    
    # Check if we can connect to VPS
    if ! ssh -o ConnectTimeout=10 -o BatchMode=yes root@$VPS_IP "echo 'Connection test'" 2>/dev/null; then
        print_error "Cannot connect to VPS at $VPS_IP"
        print_status "Please check:"
        print_status "1. VPS IP address is correct"
        print_status "2. SSH key is properly configured"
        print_status "3. VPS is running and accessible"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

backup_current_deployment() {
    print_status "Creating backup of current deployment..."
    
    ssh root@$VPS_IP << EOF
        # Create backup directory if it doesn't exist
        mkdir -p $BACKUP_DIR
        
        # Create timestamped backup
        BACKUP_NAME="astrooverz-backup-\$(date +%Y%m%d-%H%M%S)"
        
        if [ -d "$PROJECT_DIR" ]; then
            print_status "Backing up current deployment to \$BACKUP_NAME"
            cp -r $PROJECT_DIR $BACKUP_DIR/\$BACKUP_NAME
            echo "Backup created: $BACKUP_DIR/\$BACKUP_NAME"
        else
            echo "No existing deployment found to backup"
        fi
EOF
    
    print_success "Backup completed"
}

deploy_code() {
    print_status "Deploying latest code to VPS..."
    
    ssh root@$VPS_IP << EOF
        # Navigate to project directory or create it
        if [ ! -d "$PROJECT_DIR" ]; then
            print_status "Creating project directory: $PROJECT_DIR"
            mkdir -p $PROJECT_DIR
            cd $PROJECT_DIR
            git init
            git remote add origin https://github.com/Xuniverzadmin/astroo2.0.git
        else
            cd $PROJECT_DIR
        fi
        
        # Fetch latest changes
        print_status "Fetching latest changes from repository..."
        git fetch --all
        
        # Checkout and pull the feature branch
        print_status "Checking out feat/panchangam-engine branch..."
        git checkout feat/panchangam-engine || git checkout -b feat/panchangam-engine origin/feat/panchangam-engine
        git pull origin feat/panchangam-engine
        
        # Show current commit
        echo "Current commit: \$(git log --oneline -1)"
        echo "Branch: \$(git branch --show-current)"
EOF
    
    print_success "Code deployment completed"
}

setup_environment() {
    print_status "Setting up environment variables..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR
        
        # Create .env file if it doesn't exist
        if [ ! -f ".env" ]; then
            print_status "Creating .env file from template..."
            cp env.sample .env
            
            # Update with production values
            sed -i 's/POSTGRES_DB=.*/POSTGRES_DB=astrooverz/' .env
            sed -i 's/POSTGRES_USER=.*/POSTGRES_USER=astroz/' .env
            sed -i 's/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=Vettri2025/' .env
            sed -i 's/REDIS_URL=.*/REDIS_URL=redis:\/\/redis:6379/' .env
            sed -i 's/SCHED_ENABLED=.*/SCHED_ENABLED=true/' .env
            sed -i 's/CITY_PRECOMPUTE=.*/CITY_PRECOMPUTE=IN_TOP200/' .env
            sed -i 's/PRECOMPUTE_DAYS=.*/PRECOMPUTE_DAYS=30/' .env
            sed -i 's/PRECOMPUTE_TIME=.*/PRECOMPUTE_TIME=02:30/' .env
            
            print_success "Environment file created"
        else
            print_status "Environment file already exists"
        fi
        
        # Create config.env for docker-compose
        if [ ! -f "config.env" ]; then
            print_status "Creating config.env for docker-compose..."
            cp .env config.env
        fi
EOF
    
    print_success "Environment setup completed"
}

rebuild_containers() {
    print_status "Rebuilding Docker containers..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR
        
        # Stop existing containers
        print_status "Stopping existing containers..."
        docker compose down || true
        
        # Pull latest images
        print_status "Pulling latest Docker images..."
        docker compose pull || true
        
        # Build new images
        print_status "Building new Docker images..."
        docker compose build --no-cache
        
        # Start services
        print_status "Starting services..."
        docker compose up -d --remove-orphans
        
        # Wait for services to start
        print_status "Waiting for services to start..."
        sleep 30
EOF
    
    print_success "Container rebuild completed"
}

test_deployment() {
    print_status "Testing deployment..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR
        
        echo "=== Service Status ==="
        docker compose ps
        echo
        
        echo "=== Backend Health Check ==="
        if docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/healthz' 2>/dev/null; then
            echo "✅ Backend health: OK"
        else
            echo "❌ Backend health: FAILED"
        fi
        echo
        
        echo "=== API Health Check ==="
        if docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/api/healthz' 2>/dev/null; then
            echo "✅ API health: OK"
        else
            echo "❌ API health: FAILED"
        fi
        echo
        
        echo "=== Frontend Check ==="
        if docker compose exec caddy sh -c 'wget -qO- http://frontend:80/ | head -3' 2>/dev/null; then
            echo "✅ Frontend: OK"
        else
            echo "❌ Frontend: FAILED"
        fi
        echo
        
        echo "=== Caddy Routing Check ==="
        if docker compose exec caddy sh -c 'wget -qO- http://localhost/api/healthz' 2>/dev/null; then
            echo "✅ Caddy routing: OK"
        else
            echo "❌ Caddy routing: FAILED"
        fi
        echo
        
        echo "=== Public Domain Test ==="
        if curl -sS -I https://www.astrooverz.com | head -1; then
            echo "✅ Public domain: OK"
        else
            echo "❌ Public domain: FAILED"
        fi
EOF
    
    print_success "Deployment testing completed"
}

show_logs() {
    print_status "Showing recent logs..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR
        
        echo "=== Backend Logs (last 20 lines) ==="
        docker compose logs --tail=20 backend
        echo
        
        echo "=== Caddy Logs (last 10 lines) ==="
        docker compose logs --tail=10 caddy
        echo
        
        echo "=== Frontend Logs (last 10 lines) ==="
        docker compose logs --tail=10 frontend
EOF
}

rollback() {
    print_warning "Rolling back to previous deployment..."
    
    ssh root@$VPS_IP << EOF
        # Find the most recent backup
        LATEST_BACKUP=\$(ls -t $BACKUP_DIR/astrooverz-backup-* 2>/dev/null | head -1)
        
        if [ -n "\$LATEST_BACKUP" ]; then
            print_status "Rolling back to: \$LATEST_BACKUP"
            
            # Stop current services
            cd $PROJECT_DIR
            docker compose down || true
            
            # Restore backup
            rm -rf $PROJECT_DIR
            cp -r \$LATEST_BACKUP $PROJECT_DIR
            
            # Restart services
            cd $PROJECT_DIR
            docker compose up -d --remove-orphans
            
            print_success "Rollback completed"
        else
            print_error "No backup found for rollback"
        fi
EOF
}

show_help() {
    echo "VPS Deployment Script for Astrooverz.com"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  --vps-ip IP             VPS IP address"
    echo "  --project-dir DIR       Project directory on VPS (default: /opt/astrooverz)"
    echo "  --backup-dir DIR        Backup directory on VPS (default: /opt/backups)"
    echo "  --no-backup             Skip backup creation"
    echo "  --test-only             Only run tests, don't deploy"
    echo "  --rollback              Rollback to previous deployment"
    echo "  --logs                  Show recent logs"
    echo
    echo "Environment Variables:"
    echo "  VPS_IP                  VPS IP address (required)"
    echo "  PROJECT_DIR             Project directory on VPS"
    echo "  BACKUP_DIR              Backup directory on VPS"
    echo
    echo "Examples:"
    echo "  VPS_IP=192.168.1.100 $0"
    echo "  $0 --vps-ip 192.168.1.100 --no-backup"
    echo "  $0 --test-only"
    echo "  $0 --rollback"
}

main() {
    local no_backup=false
    local test_only=false
    local rollback_mode=false
    local show_logs_only=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            --vps-ip)
                VPS_IP="$2"
                shift 2
                ;;
            --project-dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            --backup-dir)
                BACKUP_DIR="$2"
                shift 2
                ;;
            --no-backup)
                no_backup=true
                shift
                ;;
            --test-only)
                test_only=true
                shift
                ;;
            --rollback)
                rollback_mode=true
                shift
                ;;
            --logs)
                show_logs_only=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    echo "=== Astrooverz.com VPS Deployment ==="
    echo "VPS IP: $VPS_IP"
    echo "Project Dir: $PROJECT_DIR"
    echo "Backup Dir: $BACKUP_DIR"
    echo
    
    if [ "$rollback_mode" = true ]; then
        rollback
        exit 0
    fi
    
    if [ "$show_logs_only" = true ]; then
        check_prerequisites
        show_logs
        exit 0
    fi
    
    if [ "$test_only" = true ]; then
        check_prerequisites
        test_deployment
        exit 0
    fi
    
    # Full deployment process
    check_prerequisites
    
    if [ "$no_backup" = false ]; then
        backup_current_deployment
    fi
    
    deploy_code
    setup_environment
    rebuild_containers
    test_deployment
    
    echo
    print_success "🎉 Deployment to astrooverz.com completed successfully!"
    echo
    print_status "Next steps:"
    print_status "1. Visit https://www.astrooverz.com to verify the site"
    print_status "2. Test the API endpoints"
    print_status "3. Monitor logs for any issues"
    print_status "4. Run '$0 --logs' to view recent logs"
    print_status "5. Run '$0 --rollback' if you need to rollback"
}

# Run main function with all arguments
main "$@"
