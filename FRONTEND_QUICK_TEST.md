# Quick Frontend Test Commands

## 🚀 Exact Command (As Requested)

### Test Frontend Through Caddy
```bash
# Ask Caddy for the homepage HTML (through the internal network)
docker compose exec caddy sh -lc 'wget -qO- http://frontend:80 | head -n 20'
```

## 🔍 Expected Results

### Frontend HTML Response (First 20 lines)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Astrooverz</title>
    <link rel="stylesheet" href="/styles.css">
    <link rel="icon" type="image/svg+xml" href="/favicon.ico">
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/main.js"></script>
</body>
</html>
```

## 🛠️ Additional Quick Tests

### Test Frontend Service Directly
```bash
# Test frontend service directly
docker compose exec frontend sh -c 'wget -qO- http://localhost:5173 | head -n 20'
```

### Test Caddy Serving
```bash
# Test Caddy serving frontend
docker compose exec caddy sh -c 'wget -qO- http://localhost:80 | head -n 20'
```

### Test External Access
```bash
# Test external access
curl -s http://localhost:80 | head -n 20
```

### Test API Proxy
```bash
# Test API proxy through Caddy
curl -s http://localhost:80/api/healthz
```

## 🚨 Quick Troubleshooting

### If Commands Fail

#### Check Service Status
```bash
# Check if services are running
docker compose ps frontend caddy

# Check service logs
docker compose logs frontend | tail -10
docker compose logs caddy | tail -10
```

#### Check Network
```bash
# Test internal connectivity
docker compose exec caddy sh -c 'curl -s http://frontend:80 | head -1'

# Check if ports are accessible
docker compose exec frontend netstat -tulpn | grep :5173
docker compose exec caddy netstat -tulpn | grep :80
```

#### Check Configuration
```bash
# Check Caddy configuration
docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile

# Check nginx configuration
docker compose exec frontend nginx -t
```

## 📊 Quick Status Check

### Service Health
```bash
# Check all services
docker compose ps

# Check specific services
docker compose ps frontend caddy
```

### Quick Health Tests
```bash
# Frontend health
docker compose exec frontend curl -f http://localhost:5173 >/dev/null && echo "Frontend OK" || echo "Frontend FAILED"

# Caddy health
docker compose exec caddy curl -f http://localhost:80 >/dev/null && echo "Caddy OK" || echo "Caddy FAILED"

# External access
curl -f http://localhost:80 >/dev/null && echo "External OK" || echo "External FAILED"
```

## 🔧 Quick Fixes

### Restart Services
```bash
# Restart frontend
docker compose restart frontend

# Restart Caddy
docker compose restart caddy

# Restart both
docker compose restart frontend caddy
```

### Check Logs
```bash
# Follow logs in real-time
docker compose logs -f frontend caddy

# Check recent errors
docker compose logs frontend | grep -i error
docker compose logs caddy | grep -i error
```

### Rebuild Frontend
```bash
# Rebuild frontend container
docker compose build --no-cache frontend
docker compose up -d frontend
```

## ✅ Success Indicators

- Frontend HTML contains `<!DOCTYPE html>` and `<title>Astrooverz</title>`
- No connection refused errors
- HTTP 200 status codes
- All services showing as "Up" in `docker compose ps`
- No errors in logs

## 🚀 Quick Test Script

### Run Simple Test
```bash
# Make script executable and run
chmod +x scripts/test-frontend-simple.sh
./scripts/test-frontend-simple.sh
```

### Run Comprehensive Test
```bash
# Make script executable and run
chmod +x scripts/test-frontend.sh
./scripts/test-frontend.sh test
```
