# Quick Debug and Deploy Commands

## 🚀 Exact Commands (As Requested)

### SSH to VPS
```bash
# SSH to VPS
ssh root@<VPS_IP>
```

### Pick the Correct Folder
```bash
# Pick the correct folder
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz
```

### Check Git Status
```bash
# Check git status
git status
```

### Fetch Latest Changes
```bash
# Fetch latest changes
git fetch --all
```

### Get Current Commit Hash
```bash
# Get current commit hash
git rev-parse --short HEAD
# Should match your latest commit locally
```

## 🔍 Expected Results

### Git Status
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

### Git Commit Hash
```
a1b2c3d
```

### Project Directory
```
/opt/astrooverz
```

## 🛠️ Additional Quick Commands

### Check Current Branch
```bash
# Check current branch
git branch
```

### Check Remote Branches
```bash
# Check remote branches
git branch -r
```

### Check Commit History
```bash
# Check commit history
git log --oneline -10
```

### Check for Uncommitted Changes
```bash
# Check for uncommitted changes
git diff --name-only
```

### Check for Untracked Files
```bash
# Check for untracked files
git status --porcelain
```

### Check Environment File
```bash
# Check environment file
ls -la .env .env.sample
```

### Show Environment File Contents
```bash
# Show environment file contents
cat .env
```

### Check Docker Services
```bash
# Check Docker services
docker compose ps
```

### Check Docker Logs
```bash
# Check Docker logs
docker compose logs --tail=20
```

### Test Backend Health
```bash
# Test backend health
curl -s http://backend:8000/healthz
```

### Test API Health
```bash
# Test API health
curl -s http://backend:8000/api/healthz
```

### Test Panchangam API
```bash
# Test panchangam API
curl -s 'http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

## 🚨 Quick Troubleshooting

### If Commands Fail

#### Check Git Configuration
```bash
# Check git configuration
git config --list

# Check remote URLs
git remote -v

# Check if repository is clean
git status --porcelain
```

#### Check Docker Services
```bash
# Check Docker daemon
docker info

# Check Docker images
docker images

# Check Docker containers
docker ps -a

# Check Docker networks
docker network ls
```

#### Check Service Logs
```bash
# Check service logs
docker compose logs backend
docker compose logs frontend
docker compose logs caddy

# Check service health
docker compose ps
```

#### Check Network Connectivity
```bash
# Check network connectivity
ping -c 4 8.8.8.8

# Check DNS resolution
nslookup www.astrooverz.com

# Check port accessibility
telnet localhost 80
telnet localhost 443
telnet localhost 8000
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

- Git status shows "working tree clean"
- Commit hash matches local commit
- Docker services show "Up" status
- Backend health check returns `{"ok": true}`
- API health check returns `{"ok": true, "status": "healthy"}`
- Public domain is accessible

## 🚀 Quick Deploy Script

### Run Simple Debug Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable and run
chmod +x scripts/debug-and-deploy-simple.sh
./scripts/debug-and-deploy-simple.sh
```

### Run Comprehensive Debug Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable and run
chmod +x scripts/debug-and-deploy.sh
./scripts/debug-and-deploy.sh debug
```

## 📝 Test Results

### Expected Output
```bash
# Git status
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

# Git commit hash
$ git rev-parse --short HEAD
a1b2c3d

# Docker services
$ docker compose ps
NAME                IMAGE                    COMMAND                  SERVICE   CREATED        STATUS                    PORTS
astrooverz-backend  astrooverz-backend:latest   "uvicorn main:app --host 0.0.0.0 --port 8000"   backend   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp
astrooverz-frontend astrooverz-frontend:latest "nginx -g 'daemon off;'"        frontend  2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5173->5173/tcp
astrooverz-caddy    astrooverz-caddy:latest     "caddy run --config /etc/caddy/Caddyfile"         caddy     2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp

# Backend health
$ curl -s http://backend:8000/healthz
{"ok": true}

# API health
$ curl -s http://backend:8000/api/healthz
{"ok": true, "status": "healthy", "service": "numerology-api"}
```
