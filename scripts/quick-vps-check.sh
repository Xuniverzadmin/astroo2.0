#!/bin/bash

# Quick VPS Check Script
# Simple script for quick VPS status and deployment checks

set -e

# Configuration
VPS_IP="${VPS_IP:-}"
PROJECT_DIR="${PROJECT_DIR:-/opt/astrooverz}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if VPS_IP is provided
if [ -z "$VPS_IP" ]; then
    print_error "VPS_IP not provided"
    echo "Usage: VPS_IP=your.vps.ip ./quick-vps-check.sh [command]"
    echo
    echo "Commands:"
    echo "  status    - Check VPS status"
    echo "  git       - Check git status"
    echo "  services  - Check Docker services"
    echo "  logs      - Show recent logs"
    echo "  update    - Update deployment"
    echo "  test      - Test deployment"
    exit 1
fi

case "${1:-status}" in
    "status")
        print_status "Checking VPS status..."
        ssh root@$VPS_IP << EOF
            echo "=== System Status ==="
            uptime
            echo
            echo "=== Memory Usage ==="
            free -h
            echo
            echo "=== Disk Usage ==="
            df -h | grep -E "(Filesystem|/dev/)"
            echo
            echo "=== Docker Services ==="
            cd $PROJECT_DIR && docker compose ps
EOF
        ;;
    
    "git")
        print_status "Checking git status..."
        ssh root@$VPS_IP << EOF
            cd $PROJECT_DIR
            echo "=== Git Status ==="
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
EOF
        ;;
    
    "services")
        print_status "Checking Docker services..."
        ssh root@$VPS_IP << EOF
            cd $PROJECT_DIR
            echo "=== Service Status ==="
            docker compose ps
            echo
            echo "=== Service Health ==="
            docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/healthz' 2>/dev/null && echo "Backend: OK" || echo "Backend: FAILED"
            docker compose exec caddy sh -c 'wget -qO- http://localhost/api/healthz' 2>/dev/null && echo "API: OK" || echo "API: FAILED"
EOF
        ;;
    
    "logs")
        print_status "Showing recent logs..."
        ssh root@$VPS_IP << EOF
            cd $PROJECT_DIR
            echo "=== Backend Logs (last 10 lines) ==="
            docker compose logs --tail=10 backend
            echo
            echo "=== Caddy Logs (last 5 lines) ==="
            docker compose logs --tail=5 caddy
EOF
        ;;
    
    "update")
        print_status "Updating VPS deployment..."
        ssh root@$VPS_IP << EOF
            cd $PROJECT_DIR
            echo "=== Pulling latest code ==="
            git fetch --all
            git reset --hard origin/main
            echo
            echo "=== Pulling Docker images ==="
            docker compose pull || true
            echo
            echo "=== Building new images ==="
            docker compose build --no-cache
            echo
            echo "=== Restarting services ==="
            docker compose down
            docker compose up -d --remove-orphans
            echo
            echo "=== Waiting for services to start ==="
            sleep 30
            docker compose ps
EOF
        print_status "Update completed"
        ;;
    
    "test")
        print_status "Testing deployment..."
        ssh root@$VPS_IP << EOF
            cd $PROJECT_DIR
            echo "=== Backend Health ==="
            docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/healthz' || echo "FAILED"
            echo
            echo "=== API Health ==="
            docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/api/healthz' || echo "FAILED"
            echo
            echo "=== Frontend ==="
            docker compose exec caddy sh -c 'wget -qO- http://frontend:80/ | head -3' || echo "FAILED"
            echo
            echo "=== Caddy Routing ==="
            docker compose exec caddy sh -c 'wget -qO- http://localhost/api/healthz' || echo "FAILED"
EOF
        print_status "Tests completed"
        ;;
    
    *)
        print_error "Unknown command: $1"
        echo "Available commands: status, git, services, logs, update, test"
        exit 1
        ;;
esac
