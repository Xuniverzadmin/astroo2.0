@echo off
REM Development and testing script for Astrooverz (Windows)
REM This script helps with local development, testing, and deployment

setlocal enabledelayedexpansion

REM Function to print colored output
:print_status
echo [INFO] %~1
goto :eof

:print_success
echo [SUCCESS] %~1
goto :eof

:print_warning
echo [WARNING] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

REM Function to check if command exists
:command_exists
where %1 >nul 2>&1
if %errorlevel% equ 0 (
    exit /b 0
) else (
    exit /b 1
)

REM Function to check prerequisites
:check_prerequisites
call :print_status "Checking prerequisites..."

set missing_deps=

where docker >nul 2>&1
if %errorlevel% neq 0 set missing_deps=%missing_deps% docker

where docker-compose >nul 2>&1
if %errorlevel% neq 0 set missing_deps=%missing_deps% docker-compose

where python >nul 2>&1
if %errorlevel% neq 0 set missing_deps=%missing_deps% python

where node >nul 2>&1
if %errorlevel% neq 0 set missing_deps=%missing_deps% node

if not "%missing_deps%"=="" (
    call :print_error "Missing dependencies:%missing_deps%"
    call :print_error "Please install the missing dependencies and try again."
    exit /b 1
)

call :print_success "All prerequisites are installed"
goto :eof

REM Function to setup development environment
:setup_dev
call :print_status "Setting up development environment..."

REM Create .env files if they don't exist
if not exist "backend\.env" (
    call :print_status "Creating backend\.env file..."
    (
        echo # Development Environment Configuration
        echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/astrooverz
        echo REDIS_URL=redis://localhost:6379
        echo.
        echo # Panchangam Configuration
        echo AYANAMSA=Lahiri
        echo MONTH_SYSTEM=Amanta
        echo DAY_BOUNDARY=sunrise
        echo.
        echo # Job Scheduling Configuration
        echo SCHED_ENABLED=false
        echo CITY_PRECOMPUTE=IN_TOP10
        echo PRECOMPUTE_DAYS=7
        echo PRECOMPUTE_TIME=02:30
        echo.
        echo # API Configuration
        echo API_V1_STR=/api
        echo PROJECT_NAME=Astrooverz Numerology API
        echo.
        echo # CORS Configuration
        echo BACKEND_CORS_ORIGINS=["*"]
        echo.
        echo # Default Timezone
        echo DEFAULT_TZ=Asia/Kolkata
    ) > backend\.env
    call :print_success "Created backend\.env file"
)

if not exist "frontend\.env" (
    call :print_status "Creating frontend\.env file..."
    (
        echo # Frontend Environment Configuration
        echo VITE_API_BASE=/api
    ) > frontend\.env
    call :print_success "Created frontend\.env file"
)

call :print_success "Development environment setup complete"
goto :eof

REM Function to install dependencies
:install_deps
call :print_status "Installing dependencies..."

REM Backend dependencies
if exist "backend\requirements.txt" (
    call :print_status "Installing Python dependencies..."
    cd backend
    python -m pip install -r requirements.txt
    cd ..
    call :print_success "Python dependencies installed"
)

REM Frontend dependencies
if exist "frontend\package.json" (
    call :print_status "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
    call :print_success "Node.js dependencies installed"
)
goto :eof

REM Function to run tests
:run_tests
call :print_status "Running tests..."

REM Backend tests
if exist "backend\tests" (
    call :print_status "Running backend tests..."
    cd backend
    python run_tests.py all
    cd ..
    call :print_success "Backend tests completed"
)

REM Frontend tests
if exist "frontend\package.json" (
    call :print_status "Running frontend tests..."
    cd frontend
    npm test 2>nul || call :print_warning "Frontend tests not configured"
    cd ..
)
goto :eof

REM Function to start development services
:start_dev
call :print_status "Starting development services..."

REM Start services with docker-compose
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

call :print_status "Waiting for services to be ready..."
timeout /t 30 /nobreak >nul

REM Check service health
curl -f http://localhost:8000/healthz >nul 2>&1
if %errorlevel% equ 0 (
    call :print_success "Backend service is healthy"
) else (
    call :print_warning "Backend service may not be ready yet"
)

curl -f http://localhost:5173 >nul 2>&1
if %errorlevel% equ 0 (
    call :print_success "Frontend service is healthy"
) else (
    call :print_warning "Frontend service may not be ready yet"
)

call :print_success "Development services started"
call :print_status "Backend: http://localhost:8000"
call :print_status "Frontend: http://localhost:5173"
call :print_status "API Health: http://localhost:8000/healthz"
goto :eof

REM Function to stop development services
:stop_dev
call :print_status "Stopping development services..."

docker-compose -f docker-compose.yml -f docker-compose.test.yml down

call :print_success "Development services stopped"
goto :eof

REM Function to build images
:build_images
call :print_status "Building Docker images..."

REM Check if docker buildx is available
docker buildx version >nul 2>&1
if %errorlevel% equ 0 (
    call :print_status "Using Docker Buildx for multi-architecture builds..."
    docker buildx bake
) else (
    call :print_status "Using standard Docker build..."
    docker-compose build
)

call :print_success "Docker images built"
goto :eof

REM Function to show help
:show_help
echo Astrooverz Development Script (Windows)
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   setup     - Setup development environment
echo   install   - Install dependencies
echo   test      - Run tests
echo   start     - Start development services
echo   stop      - Stop development services
echo   build     - Build Docker images
echo   clean     - Clean up containers and images
echo   logs      - Show service logs
echo   status    - Show service status
echo   help      - Show this help message
echo.
echo Examples:
echo   %0 setup     # Setup development environment
echo   %0 start     # Start all services
echo   %0 test      # Run all tests
echo   %0 logs      # Show service logs
goto :eof

REM Function to clean up
:clean_up
call :print_status "Cleaning up containers and images..."

docker-compose -f docker-compose.yml -f docker-compose.test.yml down -v
docker system prune -f

call :print_success "Cleanup completed"
goto :eof

REM Function to show logs
:show_logs
call :print_status "Showing service logs..."

docker-compose -f docker-compose.yml -f docker-compose.test.yml logs -f
goto :eof

REM Function to show status
:show_status
call :print_status "Service status:"

docker-compose -f docker-compose.yml -f docker-compose.test.yml ps
goto :eof

REM Main script logic
:main
if "%1"=="" goto :show_help
if "%1"=="help" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

if "%1"=="setup" (
    call :check_prerequisites
    call :setup_dev
    call :install_deps
    goto :eof
)

if "%1"=="install" (
    call :check_prerequisites
    call :install_deps
    goto :eof
)

if "%1"=="test" (
    call :check_prerequisites
    call :run_tests
    goto :eof
)

if "%1"=="start" (
    call :check_prerequisites
    call :start_dev
    goto :eof
)

if "%1"=="stop" (
    call :stop_dev
    goto :eof
)

if "%1"=="build" (
    call :check_prerequisites
    call :build_images
    goto :eof
)

if "%1"=="clean" (
    call :clean_up
    goto :eof
)

if "%1"=="logs" (
    call :show_logs
    goto :eof
)

if "%1"=="status" (
    call :show_status
    goto :eof
)

call :print_error "Unknown command: %1"
call :show_help
exit /b 1

REM Run main function
call :main %*
