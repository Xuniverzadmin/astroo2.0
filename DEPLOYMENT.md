# VPS Deployment Guide

This guide provides step-by-step instructions for deploying the Astrooverz application to your VPS.

## Prerequisites

- VPS with Ubuntu 20.04+ or similar Linux distribution
- Root or sudo access
- Docker and Docker Compose installed
- Git installed
- SSH access configured

## Quick Deployment

### 1. Connect to VPS

```bash
ssh root@<YOUR_VPS_IP>
```

### 2. Navigate to Project Directory

```bash
# Check common project directories
cd /opt/astrooverz || cd /opt/astro2.0 || cd /opt/astrooerz

# If directory doesn't exist, create it
mkdir -p /opt/astrooverz
cd /opt/astrooverz
```

### 3. Clone or Update Repository

```bash
# If repository doesn't exist, clone it
if [ ! -d ".git" ]; then
    git clone https://github.com/YOUR_USERNAME/astro2.0.git .
fi

# Update to latest code
git fetch --all
git checkout main
git pull --rebase
```

### 4. Verify Environment Configuration

```bash
# Check if .env files exist
ls -la .env .env.sample

# View current environment configuration
cat .env
```

### 5. Deploy Application

```bash
# Pull latest images
docker-compose pull

# Start services
docker-compose up -d --remove-orphans

# Check service status
docker-compose ps
```

## Detailed Setup

### Initial VPS Setup

If this is your first deployment, run the initial setup:

```bash
# Run the setup script
chmod +x scripts/vps-setup.sh
./scripts/vps-setup.sh
```

### Environment Configuration

#### Production Environment (.env)

Create or update your `.env` file:

```bash
# Copy from template
cp .env.sample .env

# Edit with your values
nano .env
```

Required environment variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://astrooverz:astrooverz123@db:5432/astrooverz

# Redis Configuration
REDIS_URL=redis://redis:6379

# Panchangam Configuration
AYANAMSA=Lahiri
MONTH_SYSTEM=Amanta
DAY_BOUNDARY=sunrise

# Job Scheduling Configuration
SCHED_ENABLED=true
CITY_PRECOMPUTE=IN_TOP200
PRECOMPUTE_DAYS=30
PRECOMPUTE_TIME=02:30

# API Configuration
API_V1_STR=/api
PROJECT_NAME=Astrooverz Numerology API

# CORS Configuration
BACKEND_CORS_ORIGINS=["*"]

# Default Timezone
DEFAULT_TZ=Asia/Kolkata
```

### Docker Compose Configuration

#### Production Override (docker-compose.prod.yml)

```yaml
version: '3.8'

services:
  backend:
    restart: unless-stopped
    environment:
      - SCHED_ENABLED=true
      - CITY_PRECOMPUTE=IN_TOP200
      - PRECOMPUTE_DAYS=30
      - PRECOMPUTE_TIME=02:30
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5173"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  caddy:
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - caddy_data:/data
      - caddy_config:/config
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:2019/config/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    restart: unless-stopped
    environment:
      - POSTGRES_DB=astrooverz
      - POSTGRES_USER=astrooverz
      - POSTGRES_PASSWORD=astrooverz123
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U astrooverz -d astrooverz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  pgdata:
  redisdata:
  caddy_data:
  caddy_config:

networks:
  web:
    driver: bridge
```

## Deployment Commands

### Start Services

```bash
# Start all services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Start with build (if needed)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Stop Services

```bash
# Stop all services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

# Stop and remove volumes (WARNING: This will delete data)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down -v
```

### Update Services

```bash
# Pull latest images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml pull

# Restart services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
```

### View Logs

```bash
# View all logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f frontend
```

### Check Status

```bash
# Check service status
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps

# Check resource usage
docker stats

# Check disk usage
df -h
```

## Health Checks

### Service Health

```bash
# Check backend health
curl -f http://localhost:8000/healthz

# Check API health
curl -f http://localhost:8000/api/healthz

# Check frontend
curl -f http://localhost:5173

# Test panchangam API
curl -f "http://localhost:8000/api/panchangam/2024-03-15?lat=13.0827&lon=80.2707&tz=Asia/Kolkata"
```

### External Access

```bash
# Test external access (replace with your VPS IP)
curl -f http://YOUR_VPS_IP/healthz

# Test API externally
curl -f "http://YOUR_VPS_IP/api/panchangam/2024-03-15?lat=13.0827&lon=80.2707&tz=Asia/Kolkata"
```

## Troubleshooting

### Common Issues

#### Services Not Starting

```bash
# Check logs for errors
docker-compose logs backend
docker-compose logs frontend

# Check if ports are in use
netstat -tulpn | grep :80
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173
```

#### Database Connection Issues

```bash
# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec db psql -U astrooverz -d astrooverz -c "SELECT 1;"
```

#### Redis Connection Issues

```bash
# Check Redis logs
docker-compose logs redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

#### Memory Issues

```bash
# Check memory usage
free -h
docker stats

# Clean up unused images
docker image prune -f
docker system prune -f
```

### Log Analysis

```bash
# View recent errors
docker-compose logs --tail=100 backend | grep -i error

# Monitor logs in real-time
docker-compose logs -f --tail=50
```

## Security Considerations

### Firewall Configuration

```bash
# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow SSH (if not already allowed)
ufw allow 22/tcp

# Enable firewall
ufw enable
```

### SSL/TLS Setup

The Caddy server automatically handles SSL certificates. Ensure your domain is properly configured:

```bash
# Check Caddy logs for SSL issues
docker-compose logs caddy | grep -i ssl
docker-compose logs caddy | grep -i certificate
```

### Regular Updates

```bash
# Update system packages
apt update && apt upgrade -y

# Update Docker images
docker-compose pull
docker-compose up -d --remove-orphans

# Clean up old images
docker image prune -f
```

## Monitoring

### Service Monitoring

```bash
# Create monitoring script
cat > /opt/astrooverz/monitor.sh << 'EOF'
#!/bin/bash
echo "=== Service Status ==="
docker-compose ps

echo "=== Resource Usage ==="
docker stats --no-stream

echo "=== Disk Usage ==="
df -h

echo "=== Memory Usage ==="
free -h
EOF

chmod +x /opt/astrooverz/monitor.sh
```

### Automated Monitoring

```bash
# Add to crontab for regular monitoring
crontab -e

# Add this line to check every 5 minutes
*/5 * * * * /opt/astrooverz/monitor.sh >> /var/log/astrooverz-monitor.log
```

## Backup and Recovery

### Database Backup

```bash
# Create backup script
cat > /opt/astrooverz/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/astrooverz/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

docker-compose exec -T db pg_dump -U astrooverz astrooverz > $BACKUP_DIR/astrooverz_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "astrooverz_*.sql" -mtime +7 -delete
EOF

chmod +x /opt/astrooverz/backup-db.sh
```

### Restore Database

```bash
# Restore from backup
docker-compose exec -T db psql -U astrooverz -d astrooverz < /opt/astrooverz/backups/astrooverz_YYYYMMDD_HHMMSS.sql
```

## Performance Optimization

### Resource Limits

Add resource limits to docker-compose.prod.yml:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### Caching

```bash
# Check Redis memory usage
docker-compose exec redis redis-cli info memory

# Monitor cache hit rates
docker-compose exec redis redis-cli info stats | grep keyspace
```

## Support

For issues and support:

1. Check the logs: `docker-compose logs -f`
2. Verify environment configuration: `cat .env`
3. Check service health: `curl -f http://localhost:8000/healthz`
4. Review this documentation
5. Check GitHub issues for known problems
