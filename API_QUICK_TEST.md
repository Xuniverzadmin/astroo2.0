# Quick API Test Commands

## 🚀 Exact Commands (As Requested)

### Inside VPS - Test Backend API
```bash
# Test health endpoint
curl -s http://backend:8000/healthz

# Test panchangam API (first 400 chars)
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata | head -c 400
```

### Alternative with Localhost
```bash
# Test health endpoint
curl -s http://localhost:8000/healthz

# Test panchangam API
curl -s http://localhost:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata | head -c 400
```

## 🔍 Expected Results

### Health Endpoint Response
```json
{"ok": true}
```

### Panchangam API Response (First 400 chars)
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

## 🛠️ Quick Troubleshooting

### If Commands Fail

#### Check Service Status
```bash
# Check if backend is running
docker compose ps backend

# Check backend logs
docker compose logs backend | tail -20
```

#### Check Network
```bash
# Test internal connectivity
docker compose exec backend curl -f http://localhost:8000/healthz

# Check if port is accessible
netstat -tulpn | grep :8000
```

#### Check Health
```bash
# Test API health endpoint
curl -s http://backend:8000/api/healthz

# Test with verbose output
curl -v http://backend:8000/healthz
```

## 📊 Additional Tests

### Test Different Dates
```bash
# Today's date
curl -s http://backend:8000/api/panchangam/$(date +%Y-%m-%d)?lat=13.0827&lon=80.2707&tz=Asia/Kolkata | head -c 400

# Different dates
curl -s http://backend:8000/api/panchangam/2024-03-15?lat=13.0827&lon=80.2707&tz=Asia/Kolkata | head -c 400
curl -s http://backend:8000/api/panchangam/2024-06-21?lat=13.0827&lon=80.2707&tz=Asia/Kolkata | head -c 400
```

### Test Different Locations
```bash
# Mumbai
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=19.0760&lon=72.8777&tz=Asia/Kolkata | head -c 400

# Delhi
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=28.7041&lon=77.1025&tz=Asia/Kolkata | head -c 400

# Bangalore
curl -s http://backend:8000/api/panchangam/2025-09-10?lat=12.9716&lon=77.5946&tz=Asia/Kolkata | head -c 400
```

### Test Performance
```bash
# Time the request
time curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata >/dev/null

# Test multiple requests
for i in {1..5}; do
  curl -s http://backend:8000/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata >/dev/null &
done
wait
```

## 🚨 Common Issues

### Connection Refused
- Backend service not running
- Port 8000 not accessible
- Network configuration issue

### 404 Not Found
- API routes not configured
- Wrong endpoint URL
- Service not properly started

### 500 Internal Server Error
- Database connection issue
- Redis connection issue
- Application error (check logs)

### Slow Response
- First request (cold start)
- Database not optimized
- Redis cache not working
- High server load

## ✅ Success Indicators

- Health endpoint returns `{"ok": true}`
- Panchangam API returns valid JSON
- Response time under 5 seconds
- No errors in logs
- All services showing as healthy
