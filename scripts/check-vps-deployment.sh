#!/bin/bash

# VPS Deployment Check Script
# This script checks VPS status, git updates, and prepares for deployment

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

check_vps_connection() {
    print_status "Checking VPS connection..."
    
    if [ -z "$VPS_IP" ]; then
        print_error "VPS_IP environment variable not set"
        print_status "Please set VPS_IP environment variable or provide as argument"
        print_status "Usage: VPS_IP=your.vps.ip ./check-vps-deployment.sh"
        exit 1
    fi
    
    if ssh -o ConnectTimeout=10 -o BatchMode=yes root@$VPS_IP "echo 'Connection successful'" 2>/dev/null; then
        print_success "VPS connection successful"
    else
        print_error "Cannot connect to VPS at $VPS_IP"
        print_status "Please check:"
        print_status "1. VPS IP address is correct"
        print_status "2. SSH key is properly configured"
        print_status "3. VPS is running and accessible"
        exit 1
    fi
}

check_git_status() {
    print_status "Checking local git status..."
    
    # Check if we're in a git repository
    if [ ! -d ".git" ]; then
        print_error "Not in a git repository"
        exit 1
    fi
    
    # Check current branch
    CURRENT_BRANCH=$(git branch --show-current)
    print_status "Current branch: $CURRENT_BRANCH"
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "You have uncommitted changes:"
        git status --short
        echo
        read -p "Do you want to commit these changes? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            read -p "Enter commit message: " commit_message
            git commit -m "$commit_message"
            print_success "Changes committed"
        else
            print_warning "Skipping uncommitted changes"
        fi
    else
        print_success "No uncommitted changes"
    fi
    
    # Check for remote updates
    print_status "Fetching remote updates..."
    git fetch --all
    
    # Check if local branch is behind remote
    if [ "$CURRENT_BRANCH" != "main" ]; then
        print_warning "You're not on main branch. Current: $CURRENT_BRANCH"
        read -p "Do you want to switch to main branch? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git checkout main
            CURRENT_BRANCH="main"
        fi
    fi
    
    # Check if behind remote
    BEHIND=$(git rev-list --count HEAD..origin/$CURRENT_BRANCH 2>/dev/null || echo "0")
    if [ "$BEHIND" -gt 0 ]; then
        print_warning "Local branch is $BEHIND commits behind remote"
        read -p "Do you want to pull latest changes? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git pull origin $CURRENT_BRANCH
            print_success "Latest changes pulled"
        fi
    else
        print_success "Local branch is up to date"
    fi
}

check_vps_git_status() {
    print_status "Checking VPS git status..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR || { echo "Project directory not found"; exit 1; }
        
        echo "=== VPS Git Status ==="
        git status --short
        echo
        
        echo "=== Current Branch ==="
        git branch --show-current
        echo
        
        echo "=== Last Commit ==="
        git log --oneline -1
        echo
        
        echo "=== Remote Status ==="
        git fetch --all
        BEHIND=\$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
        echo "Commits behind remote: \$BEHIND"
        
        if [ "\$BEHIND" -gt 0 ]; then
            echo "VPS is behind remote. Update needed."
        else
            echo "VPS is up to date."
        fi
EOF
}

check_vps_services() {
    print_status "Checking VPS services..."
    
    ssh root@$VPS_IP << EOF
        echo "=== Docker Services Status ==="
        cd $PROJECT_DIR
        docker compose ps
        echo
        
        echo "=== System Resources ==="
        echo "Memory usage:"
        free -h
        echo
        echo "Disk usage:"
        df -h
        echo
        echo "Load average:"
        uptime
EOF
}

check_vps_logs() {
    print_status "Checking recent VPS logs..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR
        echo "=== Recent Backend Logs ==="
        docker compose logs --tail=10 backend
        echo
        
        echo "=== Recent Frontend Logs ==="
        docker compose logs --tail=5 frontend
        echo
        
        echo "=== Recent Caddy Logs ==="
        docker compose logs --tail=5 caddy
EOF
}

update_vps() {
    print_status "Updating VPS deployment..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR
        
        echo "=== Pulling Latest Code ==="
        git fetch --all
        git reset --hard origin/main
        
        echo "=== Pulling Docker Images ==="
        docker compose pull || true
        
        echo "=== Building New Images ==="
        docker compose build --no-cache
        
        echo "=== Restarting Services ==="
        docker compose down
        docker compose up -d --remove-orphans
        
        echo "=== Waiting for Services to Start ==="
        sleep 30
        
        echo "=== Checking Service Health ==="
        docker compose ps
EOF
    
    print_success "VPS update completed"
}

test_deployment() {
    print_status "Testing deployment..."
    
    ssh root@$VPS_IP << EOF
        cd $PROJECT_DIR
        
        echo "=== Testing Backend Health ==="
        docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/healthz' || echo "Backend health check failed"
        
        echo "=== Testing API Health ==="
        docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/api/healthz' || echo "API health check failed"
        
        echo "=== Testing Frontend ==="
        docker compose exec caddy sh -c 'wget -qO- http://frontend:80/ | head -5' || echo "Frontend test failed"
        
        echo "=== Testing Caddy Routing ==="
        docker compose exec caddy sh -c 'wget -qO- http://localhost/api/healthz' || echo "Caddy routing test failed"
EOF
    
    print_success "Deployment tests completed"
}

show_help() {
    echo "VPS Deployment Check Script"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -c, --check-only        Only check status, don't update"
    echo "  -u, --update            Update VPS deployment"
    echo "  -t, --test              Test deployment after update"
    echo "  --vps-ip IP             VPS IP address"
    echo "  --project-dir DIR       Project directory on VPS (default: /opt/astrooverz)"
    echo
    echo "Environment Variables:"
    echo "  VPS_IP                  VPS IP address"
    echo "  PROJECT_DIR             Project directory on VPS"
    echo "  BACKUP_DIR              Backup directory on VPS"
    echo
    echo "Examples:"
    echo "  $0 --check-only"
    echo "  $0 --update --test"
    echo "  VPS_IP=192.168.1.100 $0 --update"
}

main() {
    local check_only=false
    local update=false
    local test=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--check-only)
                check_only=true
                shift
                ;;
            -u|--update)
                update=true
                shift
                ;;
            -t|--test)
                test=true
                shift
                ;;
            --vps-ip)
                VPS_IP="$2"
                shift 2
                ;;
            --project-dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    echo "=== VPS Deployment Check ==="
    echo "VPS IP: $VPS_IP"
    echo "Project Dir: $PROJECT_DIR"
    echo
    
    # Check VPS connection
    check_vps_connection
    
    # Check local git status
    check_git_status
    
    # Check VPS git status
    check_vps_git_status
    
    # Check VPS services
    check_vps_services
    
    # Check VPS logs
    check_vps_logs
    
    if [ "$check_only" = true ]; then
        print_success "Status check completed"
        exit 0
    fi
    
    if [ "$update" = true ]; then
        echo
        read -p "Do you want to proceed with VPS update? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            update_vps
            
            if [ "$test" = true ]; then
                test_deployment
            fi
        else
            print_warning "Update cancelled"
        fi
    fi
    
    print_success "All checks completed"
}

# Run main function with all arguments
main "$@"
