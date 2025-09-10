# Quick Public Domain Test Commands

## 🚀 Exact Commands (As Requested)

### Test Homepage
```bash
# From the VPS (to bypass your local cache)
curl -I https://www.astrooverz.com
```

### Test API Health
```bash
# From the VPS (to bypass your local cache)
curl -s https://www.astrooverz.com/api/healthz
```

### Test Panchangam API
```bash
# From the VPS (to bypass your local cache)
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

## 🔍 Expected Results

### Homepage Headers
```
HTTP/2 200 
content-type: text/html; charset=utf-8
content-length: 1234
server: nginx/1.21.0
date: Mon, 01 Jan 2024 12:00:00 GMT
last-modified: Mon, 01 Jan 2024 11:00:00 GMT
etag: "abc123"
accept-ranges: bytes
```

### API Health Response
```json
{
  "ok": true,
  "status": "healthy",
  "service": "numerology-api"
}
```

### Panchangam API Response (First 400 characters)
```json
{
  "date": "2025-09-10",
  "location": {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
  },
  "sunrise": "06:15:00",
  "sunset": "18:30:00",
  "tithi": {
    "name": "Chaturdashi",
    "paksha": "Krishna",
    "number": 14
  },
  "nakshatra": {
    "name": "Rohini",
    "number": 4
  }
}
```

## 🛠️ Additional Quick Tests

### Test Homepage Content
```bash
# Get homepage HTML content
curl -s https://www.astrooverz.com | head -n 20
```

### Test API Health with Headers
```bash
# Get API health headers
curl -I https://www.astrooverz.com/api/healthz
```

### Test Panchangam API with Full Response
```bash
# Get full panchangam response
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata'
```

### Test Static Assets
```bash
# Test main HTML file
curl -I https://www.astrooverz.com/index.html

# Test CSS files
curl -I https://www.astrooverz.com/styles.css

# Test JavaScript files
curl -I https://www.astrooverz.com/main.js
```

### Test SSL Certificate
```bash
# Test SSL certificate
curl -I https://www.astrooverz.com

# Test SSL with verbose output
curl -v https://www.astrooverz.com
```

### Test Domain Resolution
```bash
# Test domain resolution
nslookup www.astrooverz.com

# Test with ping
ping -c 4 www.astrooverz.com
```

## 🚨 Quick Troubleshooting

### If Commands Fail

#### Check Domain Resolution
```bash
# Check if domain resolves
nslookup www.astrooverz.com

# Check with different DNS servers
nslookup www.astrooverz.com 8.8.8.8
nslookup www.astrooverz.com 1.1.1.1
```

#### Check SSL Certificate
```bash
# Check SSL certificate
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com

# Check certificate expiration
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | openssl x509 -noout -dates
```

#### Check Network Connectivity
```bash
# Test basic connectivity
ping -c 4 www.astrooverz.com

# Test port connectivity
telnet www.astrooverz.com 443
telnet www.astrooverz.com 80
```

#### Check Response Times
```bash
# Time homepage response
time curl -s https://www.astrooverz.com >/dev/null

# Time API response
time curl -s https://www.astrooverz.com/api/healthz >/dev/null

# Time panchangam API response
time curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null
```

## 📊 Quick Status Check

### Service Health
```bash
# Check homepage
curl -f https://www.astrooverz.com >/dev/null && echo "Homepage OK" || echo "Homepage FAILED"

# Check API health
curl -f https://www.astrooverz.com/api/healthz >/dev/null && echo "API OK" || echo "API FAILED"

# Check panchangam API
curl -f 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null && echo "Panchangam API OK" || echo "Panchangam API FAILED"
```

### Quick Performance Test
```bash
# Test response times
echo "Homepage response time:"
time curl -s https://www.astrooverz.com >/dev/null

echo "API health response time:"
time curl -s https://www.astrooverz.com/api/healthz >/dev/null

echo "Panchangam API response time:"
time curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null
```

## 🔧 Quick Fixes

### Check DNS
```bash
# Flush DNS cache (if on local machine)
sudo systemctl flush-dns  # Linux
ipconfig /flushdns         # Windows
sudo dscacheutil -flushcache  # macOS
```

### Check SSL
```bash
# Test SSL certificate
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com

# Check certificate details
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | openssl x509 -noout -text
```

### Check Headers
```bash
# Check all headers
curl -I https://www.astrooverz.com

# Check specific headers
curl -s -I https://www.astrooverz.com | grep -i "content-type\|server\|date"
```

## ✅ Success Indicators

- Homepage returns `HTTP/2 200` or `HTTP/1.1 200 OK`
- API health returns `{"ok": true, "status": "healthy"}`
- Panchangam API returns valid JSON with panchangam data
- SSL certificate is valid and not expired
- Response times are under 3 seconds
- No connection refused or timeout errors

## 🚀 Quick Test Script

### Run Simple Test
```bash
# Make script executable and run
chmod +x scripts/test-public-domain-simple.sh
./scripts/test-public-domain-simple.sh
```

### Run Comprehensive Test
```bash
# Make script executable and run
chmod +x scripts/test-public-domain.sh
./scripts/test-public-domain.sh test
```

## 📝 Test Results

### Expected Output
```bash
# Homepage test
$ curl -I https://www.astrooverz.com
HTTP/2 200 
content-type: text/html; charset=utf-8
content-length: 1234
server: nginx/1.21.0
date: Mon, 01 Jan 2024 12:00:00 GMT

# API health test
$ curl -s https://www.astrooverz.com/api/healthz
{"ok": true, "status": "healthy", "service": "numerology-api"}

# Panchangam API test
$ curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
{"date": "2025-09-10", "location": {"latitude": 13.0827, "longitude": 80.2707, "timezone": "Asia/Kolkata"}, "sunrise": "06:15:00", "sunset": "18:30:00", "tithi": {"name": "Chaturdashi", "paksha": "Krishna", "number": 14}, "nakshatra": {"name": "Rohini", "number": 4}}
```
