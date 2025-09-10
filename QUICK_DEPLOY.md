# Quick VPS Deployment Guide

This is a quick reference for deploying Astrooverz to your VPS.

## 🚀 Quick Start

### 1. Connect to VPS
```bash
ssh root@<YOUR_VPS_IP>
```

### 2. Initial Setup (First Time Only)
```bash
# Download and run setup script
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/astro2.0/main/scripts/vps-setup.sh -o vps-setup.sh
chmod +x vps-setup.sh
./vps-setup.sh setup
```

### 3. Deploy Application
```bash
# Navigate to project directory
cd /opt/astrooverz

# Clone repository (if not already done)
git clone https://github.com/YOUR_USERNAME/astro2.0.git .

# Make scripts executable
chmod +x scripts/*.sh

# Deploy application
./scripts/deploy.sh deploy
```

## 📋 Step-by-Step Commands

### Pull Code & Environment
```bash
# Connect to VPS
ssh root@<YOUR_VPS_IP>

# Navigate to project directory
cd /opt/astrooverz || cd /opt/astro2.0 || cd /opt/astrooerz

# Update code
git fetch --all
git checkout main
git pull --rebase

# Verify environment
ls -la .env env.sample
cat .env
```

### Deploy Services
```bash
# Pull latest images
docker-compose pull

# Start services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans

# Check status
docker-compose ps
```

### Verify Deployment
```bash
# Check health endpoints
curl -f http://localhost:8000/healthz
curl -f http://localhost:8000/api/healthz

# Test panchangam API
curl -f "http://localhost:8000/api/panchangam/2024-03-15?lat=13.0827&lon=80.2707&tz=Asia/Kolkata"

# Check external access
curl -f http://<YOUR_VPS_IP>/healthz
```

## 🛠️ Useful Commands

### Service Management
```bash
# Check status
./scripts/deploy.sh status

# View logs
./scripts/deploy.sh logs

# Restart services
./scripts/deploy.sh restart

# Stop services
./scripts/deploy.sh stop

# Start services
./scripts/deploy.sh start
```

### Updates
```bash
# Quick update (code + images)
./scripts/deploy.sh update

# Full deployment (with backup)
./scripts/deploy.sh deploy
```

### Maintenance
```bash
# Create backup
./scripts/deploy.sh backup

# Clean up old images
./scripts/deploy.sh cleanup

# Verify deployment
./scripts/deploy.sh verify
```

## 🔧 Configuration

### Environment Variables
Edit the `.env` file with your configuration:
```bash
nano .env
```

Key variables to check:
- `DATABASE_URL`: PostgreSQL connection
- `REDIS_URL`: Redis connection
- `SCHED_ENABLED`: Background jobs (set to `true` for production)
- `CITY_PRECOMPUTE`: Cities to precompute (IN_TOP200 recommended)

### Domain Configuration
If using a custom domain:
```bash
# Update Caddyfile with your domain
nano Caddyfile

# Get SSL certificate
certbot --nginx -d yourdomain.com
```

## 📊 Monitoring

### Check Service Health
```bash
# View service status
docker-compose ps

# Check resource usage
docker stats

# View logs
docker-compose logs -f
```

### Monitor Logs
```bash
# Application logs
tail -f /var/log/astrooverz/monitor.log

# Backup logs
tail -f /var/log/astrooverz/backup.log

# System logs
journalctl -u astrooverz -f
```

## 🚨 Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Check ports
netstat -tulpn | grep :80
netstat -tulpn | grep :8000
```

#### Database Issues
```bash
# Check database logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U astrooverz -d astrooverz -c "SELECT 1;"
```

#### Memory Issues
```bash
# Check memory usage
free -h
docker stats

# Clean up
docker system prune -f
```

### Reset Everything
```bash
# Stop and remove everything
docker-compose down -v
docker system prune -a -f

# Redeploy
./scripts/deploy.sh deploy
```

## 📁 File Locations

- **Project Directory**: `/opt/astrooverz`
- **Environment File**: `/opt/astrooverz/.env`
- **Logs**: `/var/log/astrooverz/`
- **Backups**: `/opt/astrooverz/backups/`
- **Scripts**: `/opt/astrooverz/scripts/`

## 🔒 Security

### Firewall Status
```bash
# Check firewall
ufw status

# Allow ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
```

### SSL Certificates
```bash
# Check certificates
certbot certificates

# Renew certificates
certbot renew
```

## 📈 Performance

### Resource Monitoring
```bash
# System resources
htop
df -h
free -h

# Docker resources
docker stats
docker system df
```

### Optimization
```bash
# Clean up unused resources
docker system prune -f
docker volume prune -f

# Restart services
./scripts/deploy.sh restart
```

## 🆘 Support

### Get Help
1. Check logs: `./scripts/deploy.sh logs`
2. Verify health: `./scripts/deploy.sh verify`
3. Check status: `./scripts/deploy.sh status`
4. Review this guide
5. Check GitHub issues

### Emergency Commands
```bash
# Stop everything
docker-compose down

# Restart everything
./scripts/deploy.sh restart

# Full reset
docker-compose down -v && docker system prune -a -f
```

## 📝 Notes

- Replace `YOUR_USERNAME` with your GitHub username
- Replace `YOUR_VPS_IP` with your actual VPS IP address
- The setup script will configure security, monitoring, and backups automatically
- All scripts are logged to `/var/log/astrooverz-deploy.log`
- Regular backups are created daily at 2 AM
- Monitoring runs every 5 minutes
