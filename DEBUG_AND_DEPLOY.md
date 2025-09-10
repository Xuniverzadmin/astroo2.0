# Debug and Deploy Guide

This guide provides comprehensive procedures for debugging and deploying the Astrooverz application.

## 🚀 Quick Debug and Deploy Commands

### Exact Commands (As Requested)
```bash
# SSH to VPS
ssh root@<VPS_IP>

# Pick the correct folder
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz

# Check git status
git status

# Fetch latest changes
git fetch --all

# Get current commit hash
git rev-parse --short HEAD
# Should match your latest commit locally
```

### Alternative Commands
```bash
# Check current branch
git branch

# Check remote branches
git branch -r

# Check commit history
git log --oneline -10

# Check for uncommitted changes
git diff --name-only

# Check for untracked files
git status --porcelain
```

## 🛠️ Using the Debug and Deploy Scripts

### Simple Debug and Deploy Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable and run
chmod +x scripts/debug-and-deploy-simple.sh
./scripts/debug-and-deploy-simple.sh
```

### Comprehensive Debug and Deploy Script
```bash
# Set VPS IP
export VPS_IP=your_vps_ip_address

# Make script executable
chmod +x scripts/debug-and-deploy.sh

# Debug current deployment
./scripts/debug-and-deploy.sh debug

# Deploy new build
./scripts/debug-and-deploy.sh deploy

# Show deployment status
./scripts/debug-and-deploy.sh status

# Show Docker logs
./scripts/debug-and-deploy.sh logs

# Test endpoints
./scripts/debug-and-deploy.sh test

# Test public domain
./scripts/debug-and-deploy.sh public
```

## 📋 Manual Debug and Deploy Commands

### SSH and Directory Navigation
```bash
# SSH to VPS
ssh root@<VPS_IP>

# Find project directory
ls -la /opt/
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz

# Check current directory
pwd

# List directory contents
ls -la
```

### Git Status and Information
```bash
# Check git status
git status

# Check current branch
git branch

# Check remote branches
git branch -r

# Check commit history
git log --oneline -10

# Check for uncommitted changes
git diff --name-only

# Check for untracked files
git status --porcelain
```

### Fetch and Update
```bash
# Fetch latest changes
git fetch --all

# Check current commit hash
git rev-parse --short HEAD

# Check remote commit hash
git rev-parse --short origin/main

# Compare local and remote commits
git log --oneline HEAD..origin/main

# Check if local is ahead or behind
git status -uno
```

### Environment and Configuration
```bash
# Check environment file
ls -la .env .env.sample

# Show environment file contents
cat .env

# Check environment variables
env | grep -E "(DATABASE_URL|REDIS_URL|VITE_)"

# Check Docker configuration
cat docker-compose.yml | head -20
```

### Docker Services
```bash
# Check Docker services
docker compose ps

# Check Docker service health
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Check Docker logs
docker compose logs --tail=20

# Check specific service logs
docker compose logs backend --tail=20
docker compose logs frontend --tail=20
docker compose logs caddy --tail=20
```

### Container Management
```bash
# Stop all services
docker compose down

# Start all services
docker compose up -d

# Restart specific service
docker compose restart backend

# Rebuild specific service
docker compose build --no-cache backend

# Pull latest images
docker compose pull

# Remove orphaned containers
docker compose up -d --remove-orphans
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

### Docker Services Status
```
NAME                IMAGE                    COMMAND                  SERVICE   CREATED        STATUS                    PORTS
astrooverz-backend  astrooverz-backend:latest   "uvicorn main:app --host 0.0.0.0 --port 8000"   backend   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp
astrooverz-frontend astrooverz-frontend:latest "nginx -g 'daemon off;'"        frontend  2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5173->5173/tcp
astrooverz-caddy    astrooverz-caddy:latest     "caddy run --config /etc/caddy/Caddyfile"         caddy     2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

### Environment File
```
DATABASE_URL=postgresql://user:password@db:5432/astrooverz
REDIS_URL=redis://redis:6379
VITE_API_BASE_URL=https://www.astrooverz.com/api
```

## 🚨 Troubleshooting

### Common Issues

#### Git Issues
```bash
# Check git configuration
git config --list

# Check remote URLs
git remote -v

# Check if repository is clean
git status --porcelain

# Check for merge conflicts
git status | grep "both modified"

# Reset to clean state
git reset --hard HEAD
git clean -fd
```

#### Docker Issues
```bash
# Check Docker daemon
docker info

# Check Docker images
docker images

# Check Docker containers
docker ps -a

# Check Docker networks
docker network ls

# Check Docker volumes
docker volume ls

# Clean up Docker resources
docker system prune -f
```

#### Service Issues
```bash
# Check service logs
docker compose logs backend
docker compose logs frontend
docker compose logs caddy

# Check service health
docker compose ps

# Restart services
docker compose restart

# Rebuild services
docker compose build --no-cache
docker compose up -d
```

#### Network Issues
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

### Complete Deployment Test
```bash
# Run comprehensive deployment test
./scripts/debug-and-deploy.sh deploy

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

## 🚀 Deployment Steps

### Step 1: SSH and Navigate
```bash
# SSH to VPS
ssh root@<VPS_IP>

# Navigate to project directory
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz
```

### Step 2: Check Git Status
```bash
# Check git status
git status

# Fetch latest changes
git fetch --all

# Get current commit hash
git rev-parse --short HEAD
```

### Step 3: Update Code
```bash
# Check out main branch
git checkout main

# Pull latest changes
git pull --rebase

# Verify commit hash
git rev-parse --short HEAD
```

### Step 4: Check Environment
```bash
# Check environment file
ls -la .env .env.sample

# Show environment file contents
cat .env
```

### Step 5: Rebuild Containers
```bash
# Pull latest images
docker compose pull || true

# Rebuild containers
docker compose build --no-cache

# Start services
docker compose up -d --remove-orphans
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

### Rollback to Previous Commit
```bash
# Check commit history
git log --oneline -10

# Rollback to previous commit
git reset --hard HEAD~1

# Rebuild containers
docker compose build --no-cache
docker compose up -d --remove-orphans
```

### Rollback to Specific Commit
```bash
# Find specific commit
git log --oneline | grep "commit message"

# Rollback to specific commit
git reset --hard <commit-hash>

# Rebuild containers
docker compose build --no-cache
docker compose up -d --remove-orphans
```

### Emergency Rollback
```bash
# Stop all services
docker compose down

# Start with previous configuration
docker compose up -d

# Check service status
docker compose ps
```
