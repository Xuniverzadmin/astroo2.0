# Frontend Testing Guide

This guide provides comprehensive testing procedures for the Astrooverz frontend serving through Caddy.

## 🚀 Quick Frontend Tests

### Exact Command (As Requested)
```bash
# Test frontend through Caddy (exact command as requested)
docker compose exec caddy sh -lc 'wget -qO- http://frontend:80 | head -n 20'
```

### Alternative Tests
```bash
# Test frontend service directly
docker compose exec frontend sh -c 'wget -qO- http://localhost:5173 | head -n 20'

# Test Caddy serving frontend
docker compose exec caddy sh -c 'wget -qO- http://localhost:80 | head -n 20'

# Test external access
curl -s http://localhost:80 | head -n 20

# Test API proxy through Caddy
curl -s http://localhost:80/api/healthz
```

## 🛠️ Using the Testing Scripts

### Simple Frontend Test Script
```bash
# Make script executable and run
chmod +x scripts/test-frontend-simple.sh
./scripts/test-frontend-simple.sh
```

### Comprehensive Frontend Test Script
```bash
# Make script executable
chmod +x scripts/test-frontend.sh

# Test all frontend endpoints
./scripts/test-frontend.sh test

# Test frontend through Caddy (exact command)
./scripts/test-frontend.sh caddy

# Test frontend service directly
./scripts/test-frontend.sh direct

# Test external access
./scripts/test-frontend.sh external

# Test static assets
./scripts/test-frontend.sh assets

# Test API proxy through Caddy
./scripts/test-frontend.sh api-proxy

# Test Caddy configuration
./scripts/test-frontend.sh config

# Show service status
./scripts/test-frontend.sh status
```

## 📋 Manual Testing Commands

### Frontend Through Caddy
```bash
# Exact command as requested
docker compose exec caddy sh -lc 'wget -qO- http://frontend:80 | head -n 20'

# Get full HTML
docker compose exec caddy sh -c 'wget -qO- http://frontend:80'

# Check HTTP headers
docker compose exec caddy sh -c 'wget -qO- --spider -S http://frontend:80'
```

### Frontend Service Direct
```bash
# Test frontend service directly
docker compose exec frontend sh -c 'wget -qO- http://localhost:5173 | head -n 20'

# Check frontend health
docker compose exec frontend sh -c 'curl -s -I http://localhost:5173'

# Get frontend logs
docker compose logs frontend
```

### Caddy Serving
```bash
# Test Caddy serving frontend
docker compose exec caddy sh -c 'wget -qO- http://localhost:80 | head -n 20'

# Check Caddy configuration
docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile

# Get Caddy logs
docker compose logs caddy
```

### External Access
```bash
# Test external access
curl -s http://localhost:80 | head -n 20

# Check HTTP status
curl -s -I http://localhost:80

# Test with verbose output
curl -v http://localhost:80
```

### Static Assets
```bash
# Test main HTML file
curl -s -I http://localhost:80/index.html

# Test CSS files
curl -s -I http://localhost:80/styles.css

# Test JavaScript files
curl -s -I http://localhost:80/main.js

# Test favicon
curl -s -I http://localhost:80/favicon.ico
```

### API Proxy
```bash
# Test API proxy through Caddy
curl -s http://localhost:80/api/healthz

# Test backend API through Caddy
curl -s http://localhost:80/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata
```

## 🔍 Expected Results

### Frontend HTML Response
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Astrooverz</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/main.js"></script>
</body>
</html>
```

### HTTP Headers
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1234
Server: nginx/1.21.0
Date: Mon, 01 Jan 2024 12:00:00 GMT
```

### API Proxy Response
```json
{
  "ok": true,
  "status": "healthy",
  "service": "numerology-api"
}
```

## 🚨 Troubleshooting

### Common Issues

#### Frontend Not Serving
```bash
# Check if frontend container is running
docker compose ps frontend

# Check frontend logs
docker compose logs frontend

# Check if port 5173 is accessible
docker compose exec frontend netstat -tulpn | grep :5173
```

#### Caddy Not Serving
```bash
# Check if Caddy container is running
docker compose ps caddy

# Check Caddy logs
docker compose logs caddy

# Check Caddy configuration
docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile

# Check if port 80 is accessible
docker compose exec caddy netstat -tulpn | grep :80
```

#### API Proxy Not Working
```bash
# Check if backend is accessible from Caddy
docker compose exec caddy sh -c 'curl -s http://backend:8000/healthz'

# Check Caddy configuration for API proxy
docker compose exec caddy cat /etc/caddy/Caddyfile

# Check network connectivity
docker compose exec caddy ping backend
```

#### Static Assets Not Loading
```bash
# Check if assets exist in frontend container
docker compose exec frontend ls -la /usr/share/nginx/html/

# Check nginx configuration
docker compose exec frontend cat /etc/nginx/nginx.conf

# Check nginx logs
docker compose exec frontend tail -f /var/log/nginx/access.log
```

### Debug Commands

#### Check Service Status
```bash
# Check all services
docker compose ps

# Check specific services
docker compose ps frontend caddy

# Check service health
docker compose exec frontend curl -f http://localhost:5173
docker compose exec caddy curl -f http://localhost:80
```

#### Check Network Connectivity
```bash
# Test internal network
docker compose exec caddy sh -c 'curl -s http://frontend:80 | head -1'

# Test external access
curl -s http://localhost:80 | head -1

# Check DNS resolution
docker compose exec caddy nslookup frontend
docker compose exec caddy nslookup backend
```

#### Check Logs
```bash
# Frontend logs
docker compose logs frontend

# Caddy logs
docker compose logs caddy

# Follow logs in real-time
docker compose logs -f frontend caddy

# Check recent errors
docker compose logs frontend | grep -i error
docker compose logs caddy | grep -i error
```

## 📊 Performance Testing

### Response Time Testing
```bash
# Time frontend response
time curl -s http://localhost:80 >/dev/null

# Time API proxy response
time curl -s http://localhost:80/api/healthz >/dev/null

# Load test frontend
for i in {1..10}; do
  curl -s http://localhost:80 >/dev/null &
done
wait
```

### Static Asset Testing
```bash
# Test asset loading times
curl -w "@curl-format.txt" -s http://localhost:80/index.html

# Create curl format file
cat > curl-format.txt << 'EOF'
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
EOF
```

## 🔧 Configuration Testing

### Caddy Configuration
```bash
# Validate Caddy configuration
docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile

# Test Caddy configuration
docker compose exec caddy caddy test --config /etc/caddy/Caddyfile

# Reload Caddy configuration
docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
```

### Nginx Configuration
```bash
# Test nginx configuration
docker compose exec frontend nginx -t

# Reload nginx configuration
docker compose exec frontend nginx -s reload

# Check nginx status
docker compose exec frontend nginx -s status
```

### Environment Variables
```bash
# Check frontend environment
docker compose exec frontend env | grep -E "(VITE_|NODE_)"

# Check Caddy environment
docker compose exec caddy env | grep -E "(CADDY_|DOMAIN_)"
```

## 📝 Test Results Documentation

### Expected Results
- **Frontend HTML**: Should return valid HTML with React app
- **Static Assets**: Should return 200 OK for CSS, JS, and image files
- **API Proxy**: Should proxy API requests to backend service
- **Response Time**: Should be under 2 seconds for static content

### Performance Benchmarks
- **Frontend HTML**: < 1 second
- **Static Assets**: < 500ms
- **API Proxy**: < 2 seconds
- **Concurrent Requests**: Should handle 50+ concurrent requests

### Success Criteria
- Frontend serves valid HTML through Caddy
- Static assets are accessible and load quickly
- API proxy works correctly
- No 404 or 500 errors in logs
- All services are healthy and running

## 🚀 Deployment Verification

### Complete Frontend Test
```bash
# Run comprehensive frontend test
./scripts/test-frontend.sh test

# Check all services are healthy
docker compose ps

# Verify external access
curl -s http://localhost:80 | grep -q "Astrooverz" && echo "Frontend is serving correctly"
```

### Production Readiness
```bash
# Test with production-like load
for i in {1..20}; do
  curl -s http://localhost:80 >/dev/null &
  curl -s http://localhost:80/api/healthz >/dev/null &
done
wait

# Check for errors
docker compose logs frontend caddy | grep -i error | wc -l
```
