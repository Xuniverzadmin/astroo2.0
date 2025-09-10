# Background Jobs System

This document describes the background job system for precomputing panchangam data and caching.

## Overview

The job system uses APScheduler to run background tasks that precompute panchangam data for top Indian cities. This improves API response times by caching frequently requested data.

## Configuration

### Environment Variables

Add these variables to your `.env` file:

```bash
# Job Scheduling Configuration
SCHED_ENABLED=true                    # Enable/disable job scheduling
CITY_PRECOMPUTE=IN_TOP200            # Cities to precompute (IN_TOP10, IN_TOP50, IN_TOP200, ALL)
PRECOMPUTE_DAYS=30                   # Number of days to precompute ahead
PRECOMPUTE_TIME=02:30                # Time to run precompute job (IST)

# Redis Configuration (required for caching)
REDIS_URL=redis://redis:6379

# Database Configuration (optional for persistence)
DATABASE_URL=postgresql://user:pass@host:port/db
```

### City Precompute Options

- `IN_TOP10`: Precompute for top 10 Indian cities
- `IN_TOP50`: Precompute for top 50 Indian cities  
- `IN_TOP200`: Precompute for top 200 Indian cities
- `ALL`: Precompute for all configured cities

## Job Details

### Precompute Panchangam Job

**Schedule**: Daily at 02:30 IST (configurable)
**Purpose**: Precompute panchangam data for the next 30 days for top cities

**What it does**:
1. Loads configured cities based on `CITY_PRECOMPUTE` setting
2. For each city, computes panchangam data for the next 30 days
3. Stores data in Redis cache with 7-day expiration
4. Optionally stores data in PostgreSQL database
5. Computes festival data for each month
6. Stores festival data in Redis with 30-day expiration

### Cities Included

The system includes data for major Indian cities:

**Top 20 Cities**:
- Mumbai, Delhi, Bangalore, Hyderabad, Ahmedabad
- Chennai, Kolkata, Surat, Pune, Jaipur
- Lucknow, Kanpur, Nagpur, Indore, Thane
- Bhopal, Visakhapatnam, Pimpri-Chinchwad, Patna, Vadodara

**Additional Cities**:
- South Indian: Kochi, Coimbatore, Madurai, Tiruchirappalli, Salem
- North Indian: Chandigarh, Amritsar, Jalandhar, Gurgaon, Panipat
- And many more based on population and regional importance

## Data Storage

### Redis Cache

**Panchangam Data**:
- Key format: `panchangam:{city_name}:{date}`
- Expiration: 7 days
- Contains: Complete panchangam data for the date

**Festival Data**:
- Key format: `festivals:{city_name}:{year}:{month}`
- Expiration: 30 days
- Contains: Festival data for the month

**Summary Data**:
- Key: `precompute:summary`
- Expiration: 24 hours
- Contains: Last run statistics and summary

### Database Storage

**PanchangDay Table**:
- Stores precomputed panchangam data
- Used for historical queries and backup
- Indexed by date, latitude, longitude

**FestivalDay Table**:
- Stores festival information
- Used for festival calendar queries
- Indexed by date, festival type, region

## Monitoring

### Job Status

The system provides logging for:
- Job start/completion times
- Number of cities processed
- Success/failure counts
- Error details for failed computations

### Redis Monitoring

Check Redis for:
- Cache hit rates
- Memory usage
- Key expiration patterns

### Database Monitoring

Monitor database for:
- Table sizes
- Query performance
- Index usage

## Performance Benefits

### API Response Times

**Without Precomputation**:
- Panchangam calculation: 200-500ms per request
- Festival calculation: 100-300ms per request

**With Precomputation**:
- Panchangam from cache: 10-50ms per request
- Festival from cache: 5-20ms per request

### Scalability

- Reduces database load during peak hours
- Enables handling of high concurrent requests
- Provides consistent response times

## Manual Operations

### Trigger Precomputation

```python
from numerology_app.jobs import precompute_job

# Run precomputation manually
await precompute_job.precompute_panchangam()
```

### Check Job Status

```python
# Check if scheduler is running
if precompute_job.scheduler and precompute_job.scheduler.running:
    print("Scheduler is running")
    
# Get job information
jobs = precompute_job.scheduler.get_jobs()
for job in jobs:
    print(f"Job: {job.name}, Next run: {job.next_run_time}")
```

### Clear Cache

```python
# Clear all precomputed data
if precompute_job.redis_client:
    keys = await precompute_job.redis_client.keys("panchangam:*")
    if keys:
        await precompute_job.redis_client.delete(*keys)
    
    keys = await precompute_job.redis_client.keys("festivals:*")
    if keys:
        await precompute_job.redis_client.delete(*keys)
```

## Troubleshooting

### Common Issues

**Job Not Running**:
- Check `SCHED_ENABLED=true` in environment
- Verify Redis connection
- Check application logs for errors

**High Memory Usage**:
- Reduce `CITY_PRECOMPUTE` to fewer cities
- Reduce `PRECOMPUTE_DAYS` to fewer days
- Check Redis memory configuration

**Database Errors**:
- Verify database connection
- Check table permissions
- Monitor database disk space

### Logs

Check application logs for:
- Job execution details
- Error messages
- Performance metrics
- Cache statistics

## Production Deployment

### Requirements

1. **Redis Server**: Required for caching
2. **PostgreSQL**: Optional for persistence
3. **Sufficient Memory**: For Redis cache
4. **Network Access**: For city data APIs

### Deployment Steps

1. Set environment variables
2. Ensure Redis is running
3. Start application with `SCHED_ENABLED=true`
4. Monitor logs for job execution
5. Verify cache population

### Scaling

For high-traffic deployments:
- Use Redis Cluster for distributed caching
- Run multiple application instances
- Consider separate job worker processes
- Monitor and adjust city list based on usage patterns
