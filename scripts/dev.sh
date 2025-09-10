#!/bin/bash

# Development and testing script for Astrooverz
# This script helps with local development, testing, and deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if ! command_exists python3; then
        missing_deps+=("python3")
    fi
    
    if ! command_exists node; then
        missing_deps+=("node")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_error "Please install the missing dependencies and try again."
        exit 1
    fi
    
    print_success "All prerequisites are installed"
}

# Function to setup development environment
setup_dev() {
    print_status "Setting up development environment..."
    
    # Create .env files if they don't exist
    if [ ! -f backend/.env ]; then
        print_status "Creating backend/.env file..."
        cat > backend/.env << EOF
# Development Environment Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/astrooverz
REDIS_URL=redis://localhost:6379

# Panchangam Configuration
AYANAMSA=Lahiri
MONTH_SYSTEM=Amanta
DAY_BOUNDARY=sunrise

# Job Scheduling Configuration
SCHED_ENABLED=false
CITY_PRECOMPUTE=IN_TOP10
PRECOMPUTE_DAYS=7
PRECOMPUTE_TIME=02:30

# API Configuration
API_V1_STR=/api
PROJECT_NAME=Astrooverz Numerology API

# CORS Configuration
BACKEND_CORS_ORIGINS=["*"]

# Default Timezone
DEFAULT_TZ=Asia/Kolkata
EOF
        print_success "Created backend/.env file"
    fi
    
    if [ ! -f frontend/.env ]; then
        print_status "Creating frontend/.env file..."
        cat > frontend/.env << EOF
# Frontend Environment Configuration
VITE_API_BASE=/api
EOF
        print_success "Created frontend/.env file"
    fi
    
    print_success "Development environment setup complete"
}

# Function to install dependencies
install_deps() {
    print_status "Installing dependencies..."
    
    # Backend dependencies
    if [ -f backend/requirements.txt ]; then
        print_status "Installing Python dependencies..."
        cd backend
        python3 -m pip install -r requirements.txt
        cd ..
        print_success "Python dependencies installed"
    fi
    
    # Frontend dependencies
    if [ -f frontend/package.json ]; then
        print_status "Installing Node.js dependencies..."
        cd frontend
        npm install
        cd ..
        print_success "Node.js dependencies installed"
    fi
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    if [ -d backend/tests ]; then
        print_status "Running backend tests..."
        cd backend
        python3 run_tests.py all
        cd ..
        print_success "Backend tests completed"
    fi
    
    # Frontend tests
    if [ -f frontend/package.json ]; then
        print_status "Running frontend tests..."
        cd frontend
        npm test || print_warning "Frontend tests not configured"
        cd ..
    fi
}

# Function to start development services
start_dev() {
    print_status "Starting development services..."
    
    # Start services with docker-compose
    docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
    
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    if curl -f http://localhost:8000/healthz >/dev/null 2>&1; then
        print_success "Backend service is healthy"
    else
        print_warning "Backend service may not be ready yet"
    fi
    
    if curl -f http://localhost:5173 >/dev/null 2>&1; then
        print_success "Frontend service is healthy"
    else
        print_warning "Frontend service may not be ready yet"
    fi
    
    print_success "Development services started"
    print_status "Backend: http://localhost:8000"
    print_status "Frontend: http://localhost:5173"
    print_status "API Health: http://localhost:8000/healthz"
}

# Function to stop development services
stop_dev() {
    print_status "Stopping development services..."
    
    docker-compose -f docker-compose.yml -f docker-compose.test.yml down
    
    print_success "Development services stopped"
}

# Function to build images
build_images() {
    print_status "Building Docker images..."
    
    # Check if docker buildx is available
    if command_exists docker && docker buildx version >/dev/null 2>&1; then
        print_status "Using Docker Buildx for multi-architecture builds..."
        docker buildx bake
    else
        print_status "Using standard Docker build..."
        docker-compose build
    fi
    
    print_success "Docker images built"
}

# Function to run linting
run_lint() {
    print_status "Running linting..."
    
    # Backend linting
    if [ -d backend ]; then
        print_status "Running Python linting..."
        cd backend
        if command_exists black; then
            black --check numerology_app/ || print_warning "Black formatting issues found"
        fi
        if command_exists flake8; then
            flake8 numerology_app/ || print_warning "Flake8 issues found"
        fi
        cd ..
    fi
    
    # Frontend linting
    if [ -f frontend/package.json ]; then
        print_status "Running frontend linting..."
        cd frontend
        npm run lint || print_warning "Frontend linting issues found"
        cd ..
    fi
    
    print_success "Linting completed"
}

# Function to show help
show_help() {
    echo "Astrooverz Development Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     - Setup development environment"
    echo "  install   - Install dependencies"
    echo "  test      - Run tests"
    echo "  start     - Start development services"
    echo "  stop      - Stop development services"
    echo "  build     - Build Docker images"
    echo "  lint      - Run linting"
    echo "  clean     - Clean up containers and images"
    echo "  logs      - Show service logs"
    echo "  status    - Show service status"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup     # Setup development environment"
    echo "  $0 start     # Start all services"
    echo "  $0 test      # Run all tests"
    echo "  $0 logs      # Show service logs"
}

# Function to clean up
clean_up() {
    print_status "Cleaning up containers and images..."
    
    docker-compose -f docker-compose.yml -f docker-compose.test.yml down -v
    docker system prune -f
    
    print_success "Cleanup completed"
}

# Function to show logs
show_logs() {
    print_status "Showing service logs..."
    
    docker-compose -f docker-compose.yml -f docker-compose.test.yml logs -f
}

# Function to show status
show_status() {
    print_status "Service status:"
    
    docker-compose -f docker-compose.yml -f docker-compose.test.yml ps
}

# Main script logic
main() {
    case "${1:-help}" in
        setup)
            check_prerequisites
            setup_dev
            install_deps
            ;;
        install)
            check_prerequisites
            install_deps
            ;;
        test)
            check_prerequisites
            run_tests
            ;;
        start)
            check_prerequisites
            start_dev
            ;;
        stop)
            stop_dev
            ;;
        build)
            check_prerequisites
            build_images
            ;;
        lint)
            check_prerequisites
            run_lint
            ;;
        clean)
            clean_up
            ;;
        logs)
            show_logs
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
