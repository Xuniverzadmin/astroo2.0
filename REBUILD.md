# Container Rebuild Guide

This guide provides various methods to rebuild and restart containers cleanly with new code.

## 🚀 Quick Rebuild Commands

### Simple One-Liner (Exact Commands)
```bash
# Navigate to project directory
cd /opt/astrooverz

# Execute the exact commands you specified
docker compose pull || true        # pulls if you have a registry; safe to run
docker compose build --no-cache    # force rebuild with new code
docker compose up -d --remove-orphans
```

### Using the Simple Script
```bash
# Make script executable and run
chmod +x scripts/rebuild-simple.sh
./scripts/rebuild-simple.sh
```

### Using the Full Rebuild Script
```bash
# Full rebuild with backup and verification
chmod +x scripts/rebuild.sh
./scripts/rebuild.sh rebuild

# Quick rebuild without backup
./scripts/rebuild.sh quick

# Pull images only
./scripts/rebuild.sh pull

# Build containers only
./scripts/rebuild.sh build

# Restart services only
./scripts/rebuild.sh restart
```

### Using the Main Deployment Script
```bash
# Rebuild containers
./scripts/deploy.sh rebuild

# Full deployment (includes rebuild)
./scripts/deploy.sh deploy

# Quick update
./scripts/deploy.sh update
```

## 📋 Step-by-Step Process

### 1. Navigate to Project Directory
```bash
cd /opt/astrooverz || cd /opt/astro2.0 || cd /opt/astrooerz
```

### 2. Pull Latest Images (Optional)
```bash
# Safe to run even without registry
docker compose pull || true
```

### 3. Rebuild Containers
```bash
# Force rebuild without cache
docker compose build --no-cache
```

### 4. Start Services
```bash
# Start with orphan removal
docker compose up -d --remove-orphans
```

### 5. Verify Deployment
```bash
# Check service status
docker compose ps

# Check health endpoints
curl -f http://localhost:8000/healthz
curl -f http://localhost:8000/api/healthz

# View logs
docker compose logs -f
```

## 🔧 Advanced Rebuild Options

### With Database Backup
```bash
# Create backup before rebuild
./scripts/rebuild.sh rebuild
```

### With Registry Pull
```bash
# Pull from registry first
./scripts/rebuild.sh pull
./scripts/rebuild.sh build
```

### Clean Rebuild (Remove Old Images)
```bash
# Clean up old containers and images
docker container prune -f
docker image prune -f
docker compose build --no-cache
docker compose up -d --remove-orphans
```

### Production Rebuild
```bash
# Use production compose file
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull || true
docker compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
```

## 🛠️ Troubleshooting

### Services Not Starting
```bash
# Check logs for errors
docker compose logs backend
docker compose logs frontend

# Check if ports are in use
netstat -tulpn | grep :80
netstat -tulpn | grep :8000
```

### Build Failures
```bash
# Check Docker daemon
docker info

# Check disk space
df -h

# Clean up Docker system
docker system prune -f
```

### Health Check Failures
```bash
# Wait longer for services
sleep 60

# Check individual services
docker compose ps
docker compose logs --tail=50
```

## 📊 Monitoring Rebuild Process

### Real-time Monitoring
```bash
# Watch service status
watch docker compose ps

# Monitor logs
docker compose logs -f

# Check resource usage
docker stats
```

### Health Verification
```bash
# Backend health
curl -f http://localhost:8000/healthz

# API health
curl -f http://localhost:8000/api/healthz

# Frontend health
curl -f http://localhost:5173

# Panchangam API test
curl -f "http://localhost:8000/api/panchangam/2024-03-15?lat=13.0827&lon=80.2707&tz=Asia/Kolkata"
```

## 🔄 Rollback Process

### If Rebuild Fails
```bash
# Stop current services
docker compose down

# Restore from backup (if available)
docker compose up -d db
sleep 30
docker compose exec -T db psql -U astrooverz -d astrooverz < backups/latest_backup.sql

# Restart all services
docker compose up -d
```

### Quick Rollback
```bash
# Use the rollback function in scripts
./scripts/rebuild.sh rollback
```

## 📝 Best Practices

### Before Rebuild
1. **Create backup**: Always backup database before major changes
2. **Check disk space**: Ensure sufficient space for rebuild
3. **Verify code**: Make sure latest code is pulled
4. **Check dependencies**: Verify all dependencies are available

### During Rebuild
1. **Monitor logs**: Watch for errors during build process
2. **Check resources**: Monitor CPU and memory usage
3. **Verify health**: Test health endpoints after rebuild
4. **Check functionality**: Test key features

### After Rebuild
1. **Verify deployment**: Run health checks
2. **Test functionality**: Test panchangam API
3. **Monitor performance**: Check resource usage
4. **Update documentation**: Note any changes

## 🚨 Emergency Procedures

### Quick Restart
```bash
# Emergency restart without rebuild
docker compose restart
```

### Complete Reset
```bash
# Stop everything
docker compose down -v

# Remove all containers and images
docker system prune -a -f

# Rebuild from scratch
docker compose build --no-cache
docker compose up -d
```

### Service-Specific Restart
```bash
# Restart specific service
docker compose restart backend
docker compose restart frontend
docker compose restart db
```

## 📋 Command Reference

### Docker Compose Commands
```bash
# Pull images
docker compose pull

# Build containers
docker compose build
docker compose build --no-cache

# Start services
docker compose up -d
docker compose up -d --remove-orphans

# Stop services
docker compose down
docker compose down --remove-orphans

# View status
docker compose ps

# View logs
docker compose logs
docker compose logs -f
docker compose logs backend
```

### Script Commands
```bash
# Simple rebuild
./scripts/rebuild-simple.sh

# Full rebuild with backup
./scripts/rebuild.sh rebuild

# Quick rebuild
./scripts/rebuild.sh quick

# Deploy with rebuild
./scripts/deploy.sh rebuild
./scripts/deploy.sh deploy
```

## 💡 Tips and Tricks

### Faster Rebuilds
- Use `--parallel` flag for faster builds
- Use `--pull` flag to ensure latest base images
- Use `--no-cache` only when necessary

### Resource Management
- Monitor disk space during rebuilds
- Use `docker system prune` to clean up
- Set resource limits in docker-compose.yml

### Development Workflow
- Use `docker compose up --build` for development
- Use `docker compose logs -f` to monitor changes
- Use `docker compose exec` to debug containers
