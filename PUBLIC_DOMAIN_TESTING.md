# Public Domain Testing Guide

This guide provides comprehensive testing procedures for the Astrooverz public domain endpoints.

## 🚀 Quick Public Domain Tests

### Exact Commands (As Requested)
```bash
# Test homepage
curl -I https://www.astrooverz.com

# Test API health endpoint
curl -s https://www.astrooverz.com/api/healthz

# Test panchangam API
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

### Alternative Tests
```bash
# Test homepage with verbose output
curl -v https://www.astrooverz.com

# Test API health with headers
curl -I https://www.astrooverz.com/api/healthz

# Test panchangam API with full response
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata'

# Test static assets
curl -I https://www.astrooverz.com/index.html
```

## 🛠️ Using the Testing Scripts

### Simple Public Domain Test Script
```bash
# Make script executable and run
chmod +x scripts/test-public-domain-simple.sh
./scripts/test-public-domain-simple.sh
```

### Comprehensive Public Domain Test Script
```bash
# Make script executable
chmod +x scripts/test-public-domain.sh

# Test all public domain endpoints
./scripts/test-public-domain.sh test

# Test homepage only
./scripts/test-public-domain.sh homepage

# Test API health only
./scripts/test-public-domain.sh health

# Test panchangam API only
./scripts/test-public-domain.sh panchangam

# Test SSL certificate
./scripts/test-public-domain.sh ssl

# Test domain resolution
./scripts/test-public-domain.sh dns

# Test response times
./scripts/test-public-domain.sh performance

# Show service status
./scripts/test-public-domain.sh status
```

## 📋 Manual Testing Commands

### Homepage Testing
```bash
# Test homepage headers
curl -I https://www.astrooverz.com

# Test homepage content
curl -s https://www.astrooverz.com | head -n 20

# Test homepage with verbose output
curl -v https://www.astrooverz.com

# Test homepage response time
time curl -s https://www.astrooverz.com >/dev/null
```

### API Health Testing
```bash
# Test API health endpoint
curl -s https://www.astrooverz.com/api/healthz

# Test API health with headers
curl -I https://www.astrooverz.com/api/healthz

# Test API health with verbose output
curl -v https://www.astrooverz.com/api/healthz

# Test API health response time
time curl -s https://www.astrooverz.com/api/healthz >/dev/null
```

### Panchangam API Testing
```bash
# Test panchangam API (exact command)
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400

# Test panchangam API with full response
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata'

# Test panchangam API with headers
curl -I 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata'

# Test panchangam API with verbose output
curl -v 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata'
```

### SSL Certificate Testing
```bash
# Test SSL certificate
curl -I https://www.astrooverz.com

# Test SSL certificate with verbose output
curl -v https://www.astrooverz.com

# Test SSL certificate expiration
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Test SSL certificate chain
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | openssl x509 -noout -text
```

### Domain Resolution Testing
```bash
# Test domain resolution
nslookup www.astrooverz.com

# Test domain resolution with dig
dig www.astrooverz.com

# Test domain resolution with host
host www.astrooverz.com

# Test domain resolution with ping
ping -c 4 www.astrooverz.com
```

### Static Assets Testing
```bash
# Test main HTML file
curl -I https://www.astrooverz.com/index.html

# Test CSS files
curl -I https://www.astrooverz.com/styles.css

# Test JavaScript files
curl -I https://www.astrooverz.com/main.js

# Test favicon
curl -I https://www.astrooverz.com/favicon.ico

# Test robots.txt
curl -I https://www.astrooverz.com/robots.txt

# Test sitemap.xml
curl -I https://www.astrooverz.com/sitemap.xml
```

### CORS Headers Testing
```bash
# Test CORS headers
curl -H "Origin: https://example.com" -I https://www.astrooverz.com/api/healthz

# Test CORS preflight
curl -X OPTIONS -H "Origin: https://example.com" -H "Access-Control-Request-Method: GET" -I https://www.astrooverz.com/api/healthz

# Test CORS with different origins
curl -H "Origin: https://localhost:3000" -I https://www.astrooverz.com/api/healthz
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

### SSL Certificate Information
```
HTTP/2 200 
server: nginx/1.21.0
date: Mon, 01 Jan 2024 12:00:00 GMT
content-type: text/html; charset=utf-8
content-length: 1234
```

## 🚨 Troubleshooting

### Common Issues

#### Domain Not Resolving
```bash
# Check DNS resolution
nslookup www.astrooverz.com

# Check with different DNS servers
nslookup www.astrooverz.com 8.8.8.8
nslookup www.astrooverz.com 1.1.1.1

# Check domain registration
whois astrooverz.com
```

#### SSL Certificate Issues
```bash
# Check SSL certificate
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com

# Check certificate expiration
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Check certificate chain
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | openssl x509 -noout -text
```

#### API Not Responding
```bash
# Check API health
curl -s https://www.astrooverz.com/api/healthz

# Check API with verbose output
curl -v https://www.astrooverz.com/api/healthz

# Check API response time
time curl -s https://www.astrooverz.com/api/healthz

# Check API with different methods
curl -X GET https://www.astrooverz.com/api/healthz
curl -X POST https://www.astrooverz.com/api/healthz
```

#### Frontend Not Loading
```bash
# Check homepage
curl -I https://www.astrooverz.com

# Check homepage content
curl -s https://www.astrooverz.com | head -n 20

# Check static assets
curl -I https://www.astrooverz.com/index.html
curl -I https://www.astrooverz.com/styles.css
curl -I https://www.astrooverz.com/main.js
```

### Debug Commands

#### Check Network Connectivity
```bash
# Test basic connectivity
ping -c 4 www.astrooverz.com

# Test port connectivity
telnet www.astrooverz.com 443
telnet www.astrooverz.com 80

# Test with traceroute
traceroute www.astrooverz.com
```

#### Check Response Times
```bash
# Test response times
time curl -s https://www.astrooverz.com >/dev/null
time curl -s https://www.astrooverz.com/api/healthz >/dev/null
time curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null

# Test with curl timing
curl -w "@curl-format.txt" -s https://www.astrooverz.com >/dev/null
```

#### Check Headers
```bash
# Check all headers
curl -I https://www.astrooverz.com

# Check specific headers
curl -s -I https://www.astrooverz.com | grep -i "content-type\|server\|date"

# Check CORS headers
curl -H "Origin: https://example.com" -I https://www.astrooverz.com/api/healthz
```

## 📊 Performance Testing

### Response Time Testing
```bash
# Time homepage response
time curl -s https://www.astrooverz.com >/dev/null

# Time API response
time curl -s https://www.astrooverz.com/api/healthz >/dev/null

# Time panchangam API response
time curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' >/dev/null

# Load test with multiple requests
for i in {1..10}; do
  curl -s https://www.astrooverz.com >/dev/null &
done
wait
```

### Load Testing
```bash
# Test concurrent requests
for i in {1..20}; do
  curl -s https://www.astrooverz.com >/dev/null &
  curl -s https://www.astrooverz.com/api/healthz >/dev/null &
done
wait

# Test with different user agents
curl -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -s https://www.astrooverz.com >/dev/null
curl -H "User-Agent: curl/7.68.0" -s https://www.astrooverz.com >/dev/null
```

### Bandwidth Testing
```bash
# Test download speed
curl -o /dev/null -s -w "Downloaded: %{size_download} bytes in %{time_total} seconds\n" https://www.astrooverz.com

# Test upload speed (if applicable)
curl -X POST -d "test data" -s -w "Uploaded: %{size_upload} bytes in %{time_total} seconds\n" https://www.astrooverz.com/api/test
```

## 🔧 Configuration Testing

### DNS Configuration
```bash
# Check A records
dig A www.astrooverz.com

# Check AAAA records (IPv6)
dig AAAA www.astrooverz.com

# Check CNAME records
dig CNAME www.astrooverz.com

# Check MX records
dig MX astrooverz.com

# Check TXT records
dig TXT astrooverz.com
```

### SSL Configuration
```bash
# Check SSL version
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | grep "Protocol"

# Check cipher suites
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | grep "Cipher"

# Check certificate details
openssl s_client -connect www.astrooverz.com:443 -servername www.astrooverz.com < /dev/null 2>/dev/null | openssl x509 -noout -text
```

### HTTP Configuration
```bash
# Check HTTP methods
curl -X GET https://www.astrooverz.com
curl -X POST https://www.astrooverz.com
curl -X PUT https://www.astrooverz.com
curl -X DELETE https://www.astrooverz.com

# Check HTTP versions
curl --http1.1 https://www.astrooverz.com
curl --http2 https://www.astrooverz.com
```

## 📝 Test Results Documentation

### Expected Results
- **Homepage**: Should return 200 OK with HTML content
- **API Health**: Should return 200 OK with JSON health status
- **Panchangam API**: Should return 200 OK with panchangam data
- **SSL Certificate**: Should be valid and not expired
- **Response Time**: Should be under 3 seconds for all endpoints

### Performance Benchmarks
- **Homepage**: < 2 seconds
- **API Health**: < 1 second
- **Panchangam API**: < 3 seconds
- **Static Assets**: < 1 second
- **Concurrent Requests**: Should handle 100+ concurrent requests

### Success Criteria
- All endpoints return 200 OK status
- SSL certificate is valid and not expired
- Response times are within acceptable limits
- No 404 or 500 errors
- CORS headers are properly configured
- Static assets are accessible

## 🚀 Deployment Verification

### Complete Public Domain Test
```bash
# Run comprehensive public domain test
./scripts/test-public-domain.sh test

# Check all endpoints are accessible
curl -I https://www.astrooverz.com
curl -s https://www.astrooverz.com/api/healthz
curl -s 'https://www.astrooverz.com/api/panchangam/2025-09-10?lat=13.0827&lon=80.2707&tz=Asia/Kolkata' | head -c 400
```

### Production Readiness
```bash
# Test with production-like load
for i in {1..50}; do
  curl -s https://www.astrooverz.com >/dev/null &
  curl -s https://www.astrooverz.com/api/healthz >/dev/null &
done
wait

# Test with different geographic locations (if available)
curl -H "CF-IPCountry: US" -s https://www.astrooverz.com >/dev/null
curl -H "CF-IPCountry: IN" -s https://www.astrooverz.com >/dev/null
```
