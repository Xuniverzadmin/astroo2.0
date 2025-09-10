# Check Containers and Images

## 🚀 Commands to Run on Your VPS

### Basic Container and Image Check
```bash
# See containers + image timestamps
docker compose ps
docker image ls | head
```

### Detailed Container Information
```bash
# Check all containers
docker compose ps

# Check specific services
docker compose ps backend
docker compose ps frontend
docker compose ps caddy

# Check container health
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"
```

### Image Information
```bash
# Show all images with timestamps
docker image ls

# Show only first 10 images
docker image ls | head

# Show images with size information
docker image ls --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}\t{{.Size}}"

# Show only project images
docker image ls | grep astrooverz
```

### Container Resource Usage
```bash
# Check resource usage
docker stats --no-stream

# Check specific container resources
docker stats backend --no-stream
docker stats frontend --no-stream
docker stats caddy --no-stream
```

### Container Logs
```bash
# Show recent logs
docker compose logs --tail=10

# Show logs for specific service
docker compose logs backend --tail=20
docker compose logs frontend --tail=20
docker compose logs caddy --tail=20

# Follow logs in real-time
docker compose logs -f
```

## 🔍 Expected Results

### Docker Compose Services Status
```
NAME                IMAGE                    COMMAND                  SERVICE   CREATED        STATUS                    PORTS
astrooverz-backend  astrooverz-backend:latest   "uvicorn main:app --host 0.0.0.0 --port 8000"   backend   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp
astrooverz-frontend astrooverz-frontend:latest "nginx -g 'daemon off;'"        frontend  2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5173->5173/tcp
astrooverz-caddy    astrooverz-caddy:latest     "caddy run --config /etc/caddy/Caddyfile"         caddy     2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

### Docker Images
```
REPOSITORY          TAG       IMAGE ID       CREATED        SIZE
astrooverz-backend  latest    a1b2c3d4e5f6   2 hours ago    1.2GB
astrooverz-frontend latest    b2c3d4e5f6a7   2 hours ago    150MB
astrooverz-caddy    latest    c3d4e5f6a7b8   2 hours ago    50MB
postgres            15-alpine d4e5f6a7b8c9   1 day ago      200MB
redis               7-alpine  e5f6a7b8c9d0   1 day ago      30MB
```

## 🛠️ Using the Check Script

### Run the Check Script on VPS
```bash
# Make script executable
chmod +x scripts/check-containers-vps.sh

# Run the script
./scripts/check-containers-vps.sh
```

### SSH and Run Commands
```bash
# SSH to VPS
ssh root@<VPS_IP>

# Navigate to project directory
cd /opt/astrooverz || cd /opt/astroo2.0 || cd /opt/astrooerz

# Run the commands
docker compose ps
docker image ls | head
```

## 🚨 Troubleshooting

### If Docker Commands Fail

#### Check Docker Service
```bash
# Check if Docker is running
systemctl status docker

# Start Docker if not running
systemctl start docker

# Check Docker daemon
docker info
```

#### Check Docker Compose
```bash
# Check Docker Compose version
docker compose version

# Check if project is running
docker compose ps

# Check project configuration
docker compose config
```

#### Check Container Status
```bash
# Check all containers
docker ps -a

# Check container logs
docker logs <container_name>

# Check container health
docker inspect <container_name> | grep -A 10 "Health"
```

### Common Issues

#### Containers Not Running
```bash
# Check container status
docker compose ps

# Check container logs
docker compose logs

# Restart containers
docker compose restart

# Rebuild and restart
docker compose build --no-cache
docker compose up -d
```

#### Images Not Found
```bash
# Check available images
docker image ls

# Build missing images
docker compose build

# Pull latest images
docker compose pull
```

#### Resource Issues
```bash
# Check system resources
free -h
df -h
top -bn1 | head -20

# Check Docker resource usage
docker stats --no-stream

# Clean up Docker resources
docker system prune -f
```

## 📊 Performance Monitoring

### Resource Usage
```bash
# Monitor resource usage
docker stats

# Check specific container resources
docker stats backend frontend caddy

# Check system resources
htop
```

### Log Monitoring
```bash
# Monitor all logs
docker compose logs -f

# Monitor specific service logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f caddy
```

### Health Checks
```bash
# Check container health
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"

# Check service health endpoints
curl -s http://backend:8000/healthz
curl -s http://backend:8000/api/healthz
```

## 🔧 Maintenance Commands

### Clean Up
```bash
# Remove unused containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Clean up everything
docker system prune -f
```

### Update Images
```bash
# Pull latest images
docker compose pull

# Rebuild images
docker compose build --no-cache

# Restart with new images
docker compose up -d
```

### Backup and Restore
```bash
# Backup volumes
docker run --rm -v astrooverz_pgdata:/data -v $(pwd):/backup alpine tar czf /backup/pgdata-backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v astrooverz_pgdata:/data -v $(pwd):/backup alpine tar xzf /backup/pgdata-backup.tar.gz -C /data
```
