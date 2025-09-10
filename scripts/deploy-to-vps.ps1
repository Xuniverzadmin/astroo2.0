# VPS Deployment Script for Astrooverz.com (PowerShell)
# This script deploys the latest code to VPS and updates the website

param(
    [Parameter(Mandatory=$false)]
    [string]$VpsIp = $env:VPS_IP,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectDir = "/opt/astrooverz",
    
    [Parameter(Mandatory=$false)]
    [string]$BackupDir = "/opt/backups",
    
    [Parameter(Mandatory=$false)]
    [switch]$NoBackup,
    
    [Parameter(Mandatory=$false)]
    [switch]$TestOnly,
    
    [Parameter(Mandatory=$false)]
    [switch]$Rollback,
    
    [Parameter(Mandatory=$false)]
    [switch]$Logs,
    
    [Parameter(Mandatory=$false)]
    [switch]$Help
)

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Test-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    if (-not $VpsIp) {
        Write-Error "VPS_IP not provided"
        Write-Status "Please set VPS_IP environment variable or use -VpsIp parameter"
        Write-Status "Example: `$env:VPS_IP='your.vps.ip'; .\deploy-to-vps.ps1"
        exit 1
    }
    
    # Test SSH connection
    try {
        $result = ssh -o ConnectTimeout=10 -o BatchMode=yes root@$VpsIp "echo 'Connection test'" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "SSH connection failed"
        }
        Write-Success "Prerequisites check passed"
    }
    catch {
        Write-Error "Cannot connect to VPS at $VpsIp"
        Write-Status "Please check:"
        Write-Status "1. VPS IP address is correct"
        Write-Status "2. SSH key is properly configured"
        Write-Status "3. VPS is running and accessible"
        exit 1
    }
}

function Backup-CurrentDeployment {
    Write-Status "Creating backup of current deployment..."
    
    $backupScript = @"
        # Create backup directory if it doesn't exist
        mkdir -p $BackupDir
        
        # Create timestamped backup
        BACKUP_NAME="astrooverz-backup-`$(date +%Y%m%d-%H%M%S)"
        
        if [ -d "$ProjectDir" ]; then
            echo "Backing up current deployment to `$BACKUP_NAME"
            cp -r $ProjectDir $BackupDir/`$BACKUP_NAME
            echo "Backup created: $BackupDir/`$BACKUP_NAME"
        else
            echo "No existing deployment found to backup"
        fi
"@
    
    ssh root@$VpsIp $backupScript
    Write-Success "Backup completed"
}

function Deploy-Code {
    Write-Status "Deploying latest code to VPS..."
    
    $deployScript = @"
        # Navigate to project directory or create it
        if [ ! -d "$ProjectDir" ]; then
            echo "Creating project directory: $ProjectDir"
            mkdir -p $ProjectDir
            cd $ProjectDir
            git init
            git remote add origin https://github.com/Xuniverzadmin/astroo2.0.git
        else
            cd $ProjectDir
        fi
        
        # Fetch latest changes
        echo "Fetching latest changes from repository..."
        git fetch --all
        
        # Checkout and pull the feature branch
        echo "Checking out feat/panchangam-engine branch..."
        git checkout feat/panchangam-engine || git checkout -b feat/panchangam-engine origin/feat/panchangam-engine
        git pull origin feat/panchangam-engine
        
        # Show current commit
        echo "Current commit: `$(git log --oneline -1)"
        echo "Branch: `$(git branch --show-current)"
"@
    
    ssh root@$VpsIp $deployScript
    Write-Success "Code deployment completed"
}

function Setup-Environment {
    Write-Status "Setting up environment variables..."
    
    $envScript = @"
        cd $ProjectDir
        
        # Create .env file if it doesn't exist
        if [ ! -f ".env" ]; then
            echo "Creating .env file from template..."
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
            
            echo "Environment file created"
        else
            echo "Environment file already exists"
        fi
        
        # Create config.env for docker-compose
        if [ ! -f "config.env" ]; then
            echo "Creating config.env for docker-compose..."
            cp .env config.env
        fi
"@
    
    ssh root@$VpsIp $envScript
    Write-Success "Environment setup completed"
}

function Rebuild-Containers {
    Write-Status "Rebuilding Docker containers..."
    
    $rebuildScript = @"
        cd $ProjectDir
        
        # Stop existing containers
        echo "Stopping existing containers..."
        docker compose down || true
        
        # Pull latest images
        echo "Pulling latest Docker images..."
        docker compose pull || true
        
        # Build new images
        echo "Building new Docker images..."
        docker compose build --no-cache
        
        # Start services
        echo "Starting services..."
        docker compose up -d --remove-orphans
        
        # Wait for services to start
        echo "Waiting for services to start..."
        sleep 30
"@
    
    ssh root@$VpsIp $rebuildScript
    Write-Success "Container rebuild completed"
}

function Test-Deployment {
    Write-Status "Testing deployment..."
    
    $testScript = @"
        cd $ProjectDir
        
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
"@
    
    ssh root@$VpsIp $testScript
    Write-Success "Deployment testing completed"
}

function Show-Logs {
    Write-Status "Showing recent logs..."
    
    $logsScript = @"
        cd $ProjectDir
        
        echo "=== Backend Logs (last 20 lines) ==="
        docker compose logs --tail=20 backend
        echo
        
        echo "=== Caddy Logs (last 10 lines) ==="
        docker compose logs --tail=10 caddy
        echo
        
        echo "=== Frontend Logs (last 10 lines) ==="
        docker compose logs --tail=10 frontend
"@
    
    ssh root@$VpsIp $logsScript
}

function Show-Help {
    Write-Host "VPS Deployment Script for Astrooverz.com (PowerShell)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\deploy-to-vps.ps1 [OPTIONS]" -ForegroundColor White
    Write-Host ""
    Write-Host "Parameters:" -ForegroundColor Yellow
    Write-Host "  -VpsIp IP              VPS IP address" -ForegroundColor White
    Write-Host "  -ProjectDir DIR        Project directory on VPS (default: /opt/astrooverz)" -ForegroundColor White
    Write-Host "  -BackupDir DIR         Backup directory on VPS (default: /opt/backups)" -ForegroundColor White
    Write-Host "  -NoBackup              Skip backup creation" -ForegroundColor White
    Write-Host "  -TestOnly              Only run tests, don't deploy" -ForegroundColor White
    Write-Host "  -Rollback              Rollback to previous deployment" -ForegroundColor White
    Write-Host "  -Logs                  Show recent logs" -ForegroundColor White
    Write-Host "  -Help                  Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Environment Variables:" -ForegroundColor Yellow
    Write-Host "  `$env:VPS_IP           VPS IP address (required)" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  `$env:VPS_IP='192.168.1.100'; .\deploy-to-vps.ps1" -ForegroundColor White
    Write-Host "  .\deploy-to-vps.ps1 -VpsIp '192.168.1.100' -NoBackup" -ForegroundColor White
    Write-Host "  .\deploy-to-vps.ps1 -TestOnly" -ForegroundColor White
    Write-Host "  .\deploy-to-vps.ps1 -Rollback" -ForegroundColor White
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Host "=== Astrooverz.com VPS Deployment ===" -ForegroundColor Cyan
Write-Host "VPS IP: $VpsIp" -ForegroundColor White
Write-Host "Project Dir: $ProjectDir" -ForegroundColor White
Write-Host "Backup Dir: $BackupDir" -ForegroundColor White
Write-Host ""

if ($Rollback) {
    Write-Warning "Rollback functionality not implemented in PowerShell version"
    Write-Status "Please use the bash script for rollback: ./scripts/deploy-to-vps.sh --rollback"
    exit 0
}

if ($Logs) {
    Test-Prerequisites
    Show-Logs
    exit 0
}

if ($TestOnly) {
    Test-Prerequisites
    Test-Deployment
    exit 0
}

# Full deployment process
Test-Prerequisites

if (-not $NoBackup) {
    Backup-CurrentDeployment
}

Deploy-Code
Setup-Environment
Rebuild-Containers
Test-Deployment

Write-Host ""
Write-Success "🎉 Deployment to astrooverz.com completed successfully!"
Write-Host ""
Write-Status "Next steps:"
Write-Status "1. Visit https://www.astrooverz.com to verify the site"
Write-Status "2. Test the API endpoints"
Write-Status "3. Monitor logs for any issues"
Write-Status "4. Run '.\deploy-to-vps.ps1 -Logs' to view recent logs"
