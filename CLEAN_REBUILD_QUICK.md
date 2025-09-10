# Quick Clean Rebuild Commands

## 🚀 Exact Commands (As Requested)

### SSH to VPS and Navigate
```bash
# SSH to VPS
ssh root@<VPS_IP>

# Navigate to project directory
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz
```

### Pull Latest Changes
```bash
# from the repo folder on VPS
git pull --rebase
```

### Stop All Services
```bash
# Stop all services
docker compose down
```

### Build Containers
```bash
# Build containers with no cache
docker compose build --no-cache
```

### Start Services
```bash
# Start services
docker compose up -d --remove-orphans
```

### Check Service Status
```bash
# Check service status
docker compose ps
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

## 🛠️ Additional Quick Commands

### Check Git Status
```bash
# Check git status
git status

# Check current commit
git rev-parse --short HEAD

# Check for uncommitted changes
git diff --name-only
```

### Check Service Health
```bash
# Check service health
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"

# Check service logs
docker compose logs --tail=20

# Check specific service logs
docker compose logs backend --tail=20
```

### Test Endpoints
```bash
# Test backend health
curl -s http://backend:8000/healthz

# Test API health
curl -s http://backend:8000/api/healthz

# Test panchangam API
curl -s 'http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

### Test Public Domain
```bash
# Test homepage
curl -I https://www.astrooverz.com

# Test API health
curl -s https://www.astrooverz.com/api/healthz

# Test panchangam API
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

## 🚨 Quick Troubleshooting

### If Commands Fail

#### Check Git Status
```bash
# Check git status
git status

# Check for merge conflicts
git status | grep "both modified"

# Reset to clean state
git reset --hard HEAD
git clean -fd
```

#### Check Docker Services
```bash
# Check Docker daemon
docker info

# Check available space
df -h

# Clean up Docker resources
docker system prune -f
```

#### Check Service Logs
```bash
# Check service logs
docker compose logs

# Check specific service logs
docker compose logs backend
docker compose logs frontend
docker compose logs caddy
```

#### Check Network Connectivity
```bash
# Check network connectivity
ping -c 4 8.8.8.8

# Check port accessibility
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173
netstat -tulpn | grep :80
```

## 📊 Quick Status Check

### Service Health
```bash
# Check all services
docker compose ps

# Check specific service
docker compose ps backend
docker compose ps frontend
docker compose ps caddy
```

### Quick Health Tests
```bash
# Backend health
curl -f http://backend:8000/healthz >/dev/null && echo "Backend OK" || echo "Backend FAILED"

# API health
curl -f http://backend:8000/api/healthz >/dev/null && echo "API OK" || echo "API FAILED"

# Public domain
curl -f https://www.astrooverz.com >/dev/null && echo "Public Domain OK" || echo "Public Domain FAILED"
```

## 🔧 Quick Fixes

### Restart Services
```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart backend
docker compose restart frontend
docker compose restart caddy
```

### Rebuild Services
```bash
# Rebuild all services
docker compose build --no-cache
docker compose up -d

# Rebuild specific service
docker compose build --no-cache backend
docker compose up -d backend
```

### Clean Up Docker
```bash
# Clean up Docker resources
docker system prune -f

# Remove orphaned containers
docker compose up -d --remove-orphans
```

### Reset Git
```bash
# Reset to clean state
git reset --hard HEAD
git clean -fd

# Pull latest changes
git pull --rebase
```

## ✅ Success Indicators

- Git pull shows "Fast-forward" or "Already up to date"
- Docker compose down removes all containers
- Docker compose build completes without errors
- Docker compose up starts all services
- Docker compose ps shows all services as "Up" and "healthy"
- Backend health check returns `{"ok": true}`
- API health check returns `{"ok": true, "status": "healthy"}`
- Public domain is accessible

## 🚀 Quick Rebuild Script

### Run Simple Rebuild Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable and run
chmod +x scripts/clean-rebuild-simple.sh
./scripts/clean-rebuild-simple.sh
```

### Run Comprehensive Rebuild Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable and run
chmod +x scripts/clean-rebuild.sh
./scripts/clean-rebuild.sh rebuild
```

## 📝 Test Results

### Expected Output
```bash
# Git pull
$ git pull --rebase
Updating a1b2c3d..e4f5g6h
Fast-forward
 backend/requirements.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

# Docker compose down
$ docker compose down
[+] Running 4/4
 ✔ Container astrooverz-caddy    Removed
 ✔ Container astrooverz-frontend Removed
 ✔ Container astrooverz-backend  Removed
 ✔ Container astrooverz-db       Removed
 ✔ Container astrooverz-redis    Removed

# Docker compose build
$ docker compose build --no-cache
[+] Building 15.2s (15/15) FINISHED
 => [backend base] 15.2s
 => [backend development] 15.2s
 => [backend production] 15.2s
 => [frontend base] 12.1s
 => [frontend development] 12.1s
 => [frontend build] 12.1s
 => [frontend production] 12.1s
 => [caddy] 8.3s

# Docker compose up
$ docker compose up -d --remove-orphans
[+] Running 5/5
 ✔ Container astrooverz-redis    Started
 ✔ Container astrooverz-db       Started
 ✔ Container astrooverz-backend  Started
 ✔ Container astrooverz-frontend Started
 ✔ Container astrooverz-caddy    Started

# Docker compose ps
$ docker compose ps
NAME                IMAGE                    COMMAND                  SERVICE   CREATED        STATUS                    PORTS
astrooverz-backend  astrooverz-backend:latest   "uvicorn main:app --host 0.0.0.0 --port 8000"   backend   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp
astrooverz-frontend astrooverz-frontend:latest "nginx -g 'daemon off;'"        frontend  2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5173->5173/tcp
astrooverz-caddy    astrooverz-caddy:latest     "caddy run --config /etc/caddy/Caddyfile"         caddy     2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```
