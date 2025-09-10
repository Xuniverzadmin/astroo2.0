# API Testing Guide

This guide provides comprehensive testing procedures for the Astrooverz backend API.

## 🚀 Quick API Tests

### Basic Health Checks
```bash
# Test backend health endpoint
curl -s http://backend:8000/healthz

# Test API health endpoint
curl -s http://backend:8000/api/healthz

# Test with localhost (alternative)
curl -s http://localhost:8000/healthz
curl -s http://localhost:8000/api/healthz
```

### Panchangam API Test
```bash
# Test panchangam API (exact command as requested)
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata | head -c 400

# Test with localhost
curl -s http://localhost:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata | head -c 400
```

## 🛠️ Using the Testing Scripts

### Simple API Test Script
```bash
# Make script executable and run
chmod +x scripts/test-api-simple.sh
./scripts/test-api-simple.sh
```

### Comprehensive API Test Script
```bash
# Make script executable
chmod +x scripts/test-api.sh

# Test all endpoints on backend service
./scripts/test-api.sh test backend

# Test all endpoints on local service
./scripts/test-api.sh test local

# Test health endpoints only
./scripts/test-api.sh health backend

# Test panchangam API only
./scripts/test-api.sh panchangam backend

# Test performance only
./scripts/test-api.sh performance backend

# Test custom URL
./scripts/test-api.sh test http://your-domain.com
```

## 📋 Manual Testing Commands

### Health Endpoints
```bash
# Backend health
curl -s http://backend:8000/healthz
# Expected: {"ok": true}

# API health
curl -s http://backend:8000/api/healthz
# Expected: {"ok": true, "status": "healthy", "service": "numerology-api"}

# Localhost health
curl -s http://localhost:8000/healthz
curl -s http://localhost:8000/api/healthz
```

### Panchangam API Tests
```bash
# Basic panchangam request
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata

# Different dates
curl -s http://backend:8000/api/panchangam/2024-03-15?lat=13.0827&lon=80.2707&tz=Asia/Kolkata
curl -s http://backend:8000/api/panchangam/2024-06-21?lat=13.0827&lon=80.2707&tz=Asia/Kolkata
curl -s http://backend:8000/api/panchangam/2024-12-21?lat=13.0827&lon=80.2707&tz=Asia/Kolkata

# Different locations
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=19.0760&lon=72.8777&tz=Asia/Kolkata  # Mumbai
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=28.7041&lon=77.1025&tz=Asia/Kolkata  # Delhi
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=12.9716&lon=77.5946&tz=Asia/Kolkata  # Bangalore
```

### Calendar API Tests
```bash
# Monthly calendar
curl -s http://backend:8000/api/calendar/2024/3?lat=13.0827&lon=80.2707&tz=Asia/Kolkata

# Different months
curl -s http://backend:8000/api/calendar/2024/6?lat=13.0827&lon=80.2707&tz=Asia/Kolkata
curl -s http://backend:8000/api/calendar/2024/12?lat=13.0827&lon=80.2707&tz=Asia/Kolkata
```

### Festival API Tests
```bash
# Festivals for a month
curl -s http://backend:8000/api/festivals?year=2024&month=3&lat=13.0827&lon=80.2707&tz=Asia/Kolkata&region=TN

# Different regions
curl -s http://backend:8000/api/festivals?year=2024&month=3&lat=13.0827&lon=80.2707&tz=Asia/Kolkata&region=ALL
```

### Muhurtham API Tests
```bash
# Muhurtham periods
curl -s http://backend:8000/api/muhurtham?date=2024-03-15&lat=13.0827&lon=80.2707&tz=Asia/Kolkata&event_type=marriage

# Different event types
curl -s http://backend:8000/api/muhurtham?date=2024-03-15&lat=13.0827&lon=80.2707&tz=Asia/Kolkata&event_type=business
```

## 🔍 Response Validation

### Health Endpoint Response
```json
{
  "ok": true
}
```

### API Health Endpoint Response
```json
{
  "ok": true,
  "status": "healthy",
  "service": "numerology-api"
}
```

### Panchangam API Response Structure
```json
{
  "date": "2025-09-10",
  "location": {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
  },
  "sunrise": "2025-09-10T05:45:00+05:30",
  "sunset": "2025-09-10T18:15:00+05:30",
  "tithi": {
    "number": 15,
    "name": "Purnima",
    "progress": 0.75,
    "percentage": 75.0
  },
  "nakshatra": {
    "number": 14,
    "name": "Chitra",
    "progress": 0.25,
    "percentage": 25.0
  },
  "yoga": {
    "number": 14,
    "name": "Vyaghata",
    "progress": 0.50,
    "percentage": 50.0
  },
  "karana": {
    "name": "Vishti",
    "progress": 0.30,
    "percentage": 30.0
  },
  "rahu_kalam": {
    "start": "2025-09-10T09:00:00+05:30",
    "end": "2025-09-10T10:30:00+05:30",
    "duration_hours": 1.5
  },
  "yama_gandam": {
    "start": "2025-09-10T12:00:00+05:30",
    "end": "2025-09-10T13:30:00+05:30",
    "duration_hours": 1.5
  },
  "gulikai_kalam": {
    "start": "2025-09-10T15:00:00+05:30",
    "end": "2025-09-10T16:30:00+05:30",
    "duration_hours": 1.5
  },
  "horas": [
    {
      "hora_number": 1,
      "planet": "Sun",
      "start": "2025-09-10T05:45:00+05:30",
      "end": "2025-09-10T06:45:00+05:30",
      "duration": "1:00:00"
    }
  ],
  "gowri_panchangam": {
    "periods": {
      "amrutha": "06:00-07:30",
      "siddha": "07:30-09:00",
      "marana": "09:00-10:30",
      "rogam": "10:30-12:00",
      "laabha": "12:00-13:30",
      "dhanam": "13:30-15:00",
      "sugam": "15:00-16:30",
      "kantaka": "16:30-18:00"
    },
    "auspicious": ["amrutha", "siddha", "laabha", "dhanam", "sugam"],
    "inauspicious": ["marana", "rogam", "kantaka"]
  }
}
```

## 🚨 Troubleshooting

### Common Issues

#### Connection Refused
```bash
# Check if backend service is running
docker compose ps backend

# Check backend logs
docker compose logs backend

# Check if port 8000 is accessible
netstat -tulpn | grep :8000
```

#### 404 Not Found
```bash
# Check if API routes are properly configured
curl -s http://backend:8000/docs  # Should show API documentation

# Check if the endpoint exists
curl -s http://backend:8000/api/  # Should return API info
```

#### 500 Internal Server Error
```bash
# Check backend logs for errors
docker compose logs backend | tail -50

# Check database connection
docker compose exec backend python -c "from numerology_app.db import check_database_connection; print(check_database_connection())"

# Check Redis connection
docker compose exec backend python -c "import redis; r = redis.from_url('redis://redis:6379'); print(r.ping())"
```

#### Slow Response Times
```bash
# Check resource usage
docker stats backend

# Check if precomputation is working
docker compose logs backend | grep -i precompute

# Check Redis cache
docker compose exec redis redis-cli info memory
```

### Debug Commands

#### Check Service Status
```bash
# Check all services
docker compose ps

# Check specific service
docker compose ps backend

# Check service health
docker compose exec backend curl -f http://localhost:8000/healthz
```

#### Check Logs
```bash
# Backend logs
docker compose logs backend

# Follow logs in real-time
docker compose logs -f backend

# Check recent errors
docker compose logs backend | grep -i error
```

#### Check Network Connectivity
```bash
# Test internal network
docker compose exec backend curl -f http://backend:8000/healthz

# Test external access
curl -f http://localhost:8000/healthz

# Check DNS resolution
docker compose exec backend nslookup backend
```

## 📊 Performance Testing

### Load Testing
```bash
# Simple load test with curl
for i in {1..10}; do
  curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata >/dev/null &
done
wait

# Time a single request
time curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata >/dev/null
```

### Response Time Testing
```bash
# Test response times
curl -w "@curl-format.txt" -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata

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

## 🔧 API Configuration

### Environment Variables
```bash
# Check environment variables
docker compose exec backend env | grep -E "(DATABASE_URL|REDIS_URL|SCHED_ENABLED)"

# Check API configuration
docker compose exec backend python -c "from numerology_app.config import settings; print(f'API_V1_STR: {settings.API_V1_STR}')"
```

### Database Connection
```bash
# Test database connection
docker compose exec backend python -c "
from numerology_app.db import check_database_connection
print('Database connection:', check_database_connection())
"

# Check database tables
docker compose exec db psql -U astrooverz -d astrooverz -c "\dt"
```

### Redis Connection
```bash
# Test Redis connection
docker compose exec redis redis-cli ping

# Check Redis info
docker compose exec redis redis-cli info

# Check cached data
docker compose exec redis redis-cli keys "panchangam:*" | head -5
```

## 📝 Test Results Documentation

### Expected Results
- **Health endpoints**: Should return 200 OK with JSON response
- **Panchangam API**: Should return 200 OK with complete panchangam data
- **Response time**: Should be under 5 seconds for panchangam requests
- **Error handling**: Should return appropriate HTTP status codes

### Performance Benchmarks
- **Health check**: < 1 second
- **Panchangam calculation**: < 5 seconds
- **Cached requests**: < 1 second
- **Concurrent requests**: Should handle 10+ concurrent requests

### Success Criteria
- All health endpoints return 200 OK
- Panchangam API returns valid JSON with all required fields
- Response times meet performance benchmarks
- No 500 errors in logs
- Database and Redis connections are healthy
