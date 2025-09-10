# Clean Rebuild and Restart Guide

This guide provides comprehensive procedures for performing a clean rebuild and restart of the Astrooverz application.

## 🚀 Quick Clean Rebuild Commands

### Exact Commands (As Requested)
```bash
# from the repo folder on VPS
git pull --rebase
docker compose down
docker compose build --no-cache
docker compose up -d --remove-orphans
docker compose ps
```

### Alternative Commands
```bash
# Pull latest changes
git pull --rebase

# Stop all services
docker compose down

# Remove all containers and networks
docker compose down --volumes --remove-orphans

# Build containers with no cache
docker compose build --no-cache

# Start services
docker compose up -d --remove-orphans

# Check service status
docker compose ps

# Check service health
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"
```

## 🛠️ Using the Clean Rebuild Scripts

### Simple Clean Rebuild Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable and run
chmod +x scripts/clean-rebuild-simple.sh
./scripts/clean-rebuild-simple.sh
```

### Comprehensive Clean Rebuild Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable
chmod +x scripts/clean-rebuild.sh

# Perform clean rebuild and restart
./scripts/clean-rebuild.sh rebuild

# Pull latest changes only
./scripts/clean-rebuild.sh pull

# Stop all services only
./scripts/clean-rebuild.sh stop

# Build containers only
./scripts/clean-rebuild.sh build

# Start services only
./scripts/clean-rebuild.sh start

# Check service status only
./scripts/clean-rebuild.sh status

# Test endpoints only
./scripts/clean-rebuild.sh test
```

## 📋 Manual Clean Rebuild Commands

### SSH and Navigate
```bash
# SSH to VPS
ssh root@<VPS_IP>

# Navigate to project directory
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz

# Check current directory
pwd

# List directory contents
ls -la
```

### Pull Latest Changes
```bash
# Pull latest changes
git pull --rebase

# Check git status
git status

# Check current commit
git rev-parse --short HEAD

# Check for uncommitted changes
git diff --name-only
```

### Stop All Services
```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down --volumes

# Stop and remove orphaned containers
docker compose down --remove-orphans

# Stop and remove everything
docker compose down --volumes --remove-orphans
```

### Build Containers
```bash
# Build containers with no cache
docker compose build --no-cache

# Build specific service
docker compose build --no-cache backend

# Build with parallel processing
docker compose build --no-cache --parallel

# Build and tag
docker compose build --no-cache --tag latest
```

### Start Services
```bash
# Start services
docker compose up -d --remove-orphans

# Start with force recreate
docker compose up -d --force-recreate

# Start with no dependencies
docker compose up -d --no-deps

# Start specific service
docker compose up -d backend
```

### Check Service Status
```bash
# Check service status
docker compose ps

# Check with health status
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"

# Check service logs
docker compose logs --tail=20

# Check specific service logs
docker compose logs backend --tail=20
```

## 🔍 Expected Results

### Git Pull
```
Updating a1b2c3d..e4f5g6h
Fast-forward
 backend/requirements.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### Docker Compose Down
```
[+] Running 4/4
 ✔ Container astrooverz-caddy    Removed
 ✔ Container astrooverz-frontend Removed
 ✔ Container astrooverz-backend  Removed
 ✔ Container astrooverz-db       Removed
 ✔ Container astrooverz-redis    Removed
```

### Docker Compose Build
```
[+] Building 15.2s (15/15) FINISHED
 => [backend base] 15.2s
 => [backend development] 15.2s
 => [backend production] 15.2s
 => [frontend base] 12.1s
 => [frontend development] 12.1s
 => [frontend build] 12.1s
 => [frontend production] 12.1s
 => [caddy] 8.3s
```

### Docker Compose Up
```
[+] Running 5/5
 ✔ Container astrooverz-redis    Started
 ✔ Container astrooverz-db       Started
 ✔ Container astrooverz-backend  Started
 ✔ Container astrooverz-frontend Started
 ✔ Container astrooverz-caddy    Started
```

### Docker Compose PS
```
NAME                IMAGE                    COMMAND                  SERVICE   CREATED        STATUS                    PORTS
astrooverz-backend  astrooverz-backend:latest   "uvicorn main:app --host 0.0.0.0 --port 8000"   backend   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp
astrooverz-frontend astrooverz-frontend:latest "nginx -g 'daemon off;'"        frontend  2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5173->5173/tcp
astrooverz-caddy    astrooverz-caddy:latest     "caddy run --config /etc/caddy/Caddyfile"         caddy     2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

## 🚨 Troubleshooting

### Common Issues

#### Git Pull Issues
```bash
# Check git status
git status

# Check for merge conflicts
git status | grep "both modified"

# Reset to clean state
git reset --hard HEAD
git clean -fd

# Pull with force
git pull --rebase --force
```

#### Docker Build Issues
```bash
# Check Docker daemon
docker info

# Check available space
df -h

# Clean up Docker resources
docker system prune -f

# Check build logs
docker compose build --no-cache --progress=plain
```

#### Service Start Issues
```bash
# Check service logs
docker compose logs

# Check specific service logs
docker compose logs backend
docker compose logs frontend
docker compose logs caddy

# Check service configuration
docker compose config
```

#### Network Issues
```bash
# Check Docker networks
docker network ls

# Check network connectivity
docker compose exec backend ping frontend
docker compose exec backend ping caddy

# Check port accessibility
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173
netstat -tulpn | grep :80
```

### Debug Commands

#### Check Service Status
```bash
# Check all services
docker compose ps

# Check specific service
docker compose ps backend
docker compose ps frontend
docker compose ps caddy

# Check service health
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"
```

#### Check Logs
```bash
# Check all logs
docker compose logs

# Check specific service logs
docker compose logs backend --tail=50
docker compose logs frontend --tail=50
docker compose logs caddy --tail=50

# Follow logs in real-time
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f caddy
```

#### Check Configuration
```bash
# Check Docker Compose configuration
docker compose config

# Check environment variables
docker compose config --services

# Check service configuration
docker compose config backend
docker compose config frontend
docker compose config caddy
```

## 📊 Performance Testing

### Response Time Testing
```bash
# Test backend response time
time curl -s http://backend:8000/healthz

# Test frontend response time
time curl -s http://frontend:5173

# Test public domain response time
time curl -s https://www.astrooverz.com

# Test API response time
time curl -s https://www.astrooverz.com/api/healthz
```

### Load Testing
```bash
# Test concurrent requests
for i in {1..10}; do
  curl -s http://backend:8000/healthz >/dev/null &
done
wait

# Test with different endpoints
for i in {1..5}; do
  curl -s http://backend:8000/api/healthz >/dev/null &
  curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata >/dev/null &
done
wait
```

### Resource Usage
```bash
# Check container resource usage
docker stats --no-stream

# Check specific container resources
docker stats backend --no-stream
docker stats frontend --no-stream
docker stats caddy --no-stream

# Check system resources
free -h
df -h
top -bn1 | head -20
```

## 🔧 Configuration Testing

### Environment Variables
```bash
# Check environment variables
env | grep -E "(DATABASE_URL|REDIS_URL|VITE_)"

# Check Docker environment
docker compose config --services | xargs -I {} docker compose exec {} env

# Check specific service environment
docker compose exec backend env
docker compose exec frontend env
docker compose exec caddy env
```

### Network Configuration
```bash
# Check Docker networks
docker network ls

# Check network details
docker network inspect astrooverz_web

# Check container network
docker compose exec backend ip addr
docker compose exec frontend ip addr
docker compose exec caddy ip addr
```

### Volume Configuration
```bash
# Check Docker volumes
docker volume ls

# Check volume details
docker volume inspect astrooverz_pgdata
docker volume inspect astrooverz_redisdata

# Check volume usage
docker system df -v
```

## 📝 Deployment Verification

### Complete Clean Rebuild Test
```bash
# Run comprehensive clean rebuild
./scripts/clean-rebuild.sh rebuild

# Check all services are healthy
docker compose ps

# Verify external access
curl -I https://www.astrooverz.com
curl -s https://www.astrooverz.com/api/healthz
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

### Production Readiness
```bash
# Test with production-like load
for i in {1..20}; do
  curl -s https://www.astrooverz.com >/dev/null &
  curl -s https://www.astrooverz.com/api/healthz >/dev/null &
done
wait

# Check for errors
docker compose logs | grep -i error | wc -l

# Check resource usage
docker stats --no-stream
```

## 🚀 Clean Rebuild Steps

### Step 1: SSH and Navigate
```bash
# SSH to VPS
ssh root@<VPS_IP>

# Navigate to project directory
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz
```

### Step 2: Pull Latest Changes
```bash
# Pull latest changes
git pull --rebase

# Check git status
git status

# Verify commit hash
git rev-parse --short HEAD
```

### Step 3: Stop All Services
```bash
# Stop all services
docker compose down

# Verify services are stopped
docker compose ps
```

### Step 4: Build Containers
```bash
# Build containers with no cache
docker compose build --no-cache

# Verify build completed
docker image ls | grep astrooverz
```

### Step 5: Start Services
```bash
# Start services
docker compose up -d --remove-orphans

# Verify services are running
docker compose ps
```

### Step 6: Verify Deployment
```bash
# Check service status
docker compose ps

# Test endpoints
curl -s http://backend:8000/healthz
curl -s http://backend:8000/api/healthz
curl -s 'http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400

# Test public domain
curl -I https://www.astrooverz.com
curl -s https://www.astrooverz.com/api/healthz
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

## 🔄 Rollback Procedures

### Rollback to Previous Build
```bash
# Stop current services
docker compose down

# Check previous images
docker image ls | grep astrooverz

# Use previous image tags
docker compose up -d --remove-orphans
```

### Emergency Rollback
```bash
# Stop all services
docker compose down

# Remove current images
docker image rm astrooverz-backend:latest astrooverz-frontend:latest astrooverz-caddy:latest

# Rebuild from previous commit
git reset --hard HEAD~1
docker compose build --no-cache
docker compose up -d --remove-orphans
```

### Gradual Rollback
```bash
# Stop specific service
docker compose stop backend

# Rebuild specific service
docker compose build --no-cache backend

# Start specific service
docker compose up -d backend
```
