# Manual VPS Deployment Steps

## Prerequisites
- VPS IP address
- SSH access to VPS
- Docker and Docker Compose installed on VPS

## Step-by-Step Deployment

### 1. SSH to VPS
```bash
ssh root@YOUR_VPS_IP
```

### 2. Navigate to Project Directory
```bash
cd /opt/astrooverz
```

### 3. Check Current Status
```bash
# Check current branch and commit
git status
git branch --show-current
git log --oneline -1

# Check Docker services
docker compose ps
```

### 4. Create Backup (Optional but Recommended)
```bash
# Create backup directory
mkdir -p /opt/backups

# Create timestamped backup
BACKUP_NAME="astrooverz-backup-$(date +%Y%m%d-%H%M%S)"
cp -r /opt/astrooverz /opt/backups/$BACKUP_NAME
echo "Backup created: /opt/backups/$BACKUP_NAME"
```

### 5. Pull Latest Code
```bash
# Fetch latest changes
git fetch --all

# Checkout feature branch
git checkout feat/panchangam-engine || git checkout -b feat/panchangam-engine origin/feat/panchangam-engine

# Pull latest changes
git pull origin feat/panchangam-engine

# Verify current commit
git log --oneline -1
```

### 6. Setup Environment
```bash
# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp env.sample .env
    echo "Environment file created"
fi

# Create config.env for docker-compose
if [ ! -f "config.env" ]; then
    cp .env config.env
    echo "Config file created"
fi
```

### 7. Rebuild and Restart Containers
```bash
# Stop existing containers
docker compose down

# Pull latest images
docker compose pull || true

# Build new images
docker compose build --no-cache

# Start services
docker compose up -d --remove-orphans

# Wait for services to start
sleep 30
```

### 8. Test Deployment
```bash
# Check service status
docker compose ps

# Test backend health
docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/healthz'

# Test API health
docker compose exec backend sh -c 'curl -sS http://127.0.0.1:8000/api/healthz'

# Test frontend
docker compose exec caddy sh -c 'wget -qO- http://frontend:80/ | head -3'

# Test Caddy routing
docker compose exec caddy sh -c 'wget -qO- http://localhost/api/healthz'

# Test public domain
curl -sS -I https://www.astrooverz.com | head -1
```

### 9. View Logs (if needed)
```bash
# Backend logs
docker compose logs --tail=20 backend

# Caddy logs
docker compose logs --tail=10 caddy

# Frontend logs
docker compose logs --tail=10 frontend
```

## Troubleshooting

### If Services Fail to Start
```bash
# Check logs
docker compose logs

# Restart specific service
docker compose restart backend
docker compose restart frontend
docker compose restart caddy
```

### If Database Issues
```bash
# Check database connection
docker compose exec db psql -U astroz -d astrooverz -c "SELECT 1;"

# Restart database
docker compose restart db
```

### If CORS Issues
```bash
# Check backend logs for CORS errors
docker compose logs backend | grep -i cors
```

### Rollback (if needed)
```bash
# Stop current services
docker compose down

# Restore from backup
LATEST_BACKUP=$(ls -t /opt/backups/astrooverz-backup-* | head -1)
rm -rf /opt/astrooverz
cp -r $LATEST_BACKUP /opt/astrooverz

# Restart services
cd /opt/astrooverz
docker compose up -d --remove-orphans
```

## Verification Checklist

After deployment, verify:
- [ ] https://www.astrooverz.com loads correctly
- [ ] https://www.astrooverz.com/api/healthz returns `{"ok":true}`
- [ ] Panchangam API works: `/api/panchangam/2025-01-10`
- [ ] Frontend can make API calls without CORS errors
- [ ] All Docker services show "healthy" status
- [ ] SSL certificates are valid
- [ ] No errors in logs
