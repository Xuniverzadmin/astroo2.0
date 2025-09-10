from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import logging
import redis.asyncio as redis

from .core import analyze_name
from .panchangam.core import assemble_panchangam
from .festivals.service import festival_service
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Astrooverz API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Astrooverz Numerology API", "status": "running"}

@app.get("/healthz")
def healthz():
    return {"ok": True, "status": "healthy", "service": "numerology-api"}

@app.get("/api/healthz")
def api_healthz():
    return {"ok": True, "status": "healthy", "service": "numerology-api"}

@app.post("/api/analyze_name")
def analyze_name_endpoint(payload: NameIn):
    try:
        if not payload.name or not payload.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        result = analyze_name(payload.name.strip())
        logger.info(f"Successfully analyzed name: {payload.name}")
        return result
    except Exception as e:
        logger.error(f"Error analyzing name '{payload.name}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during name analysis")

@app.get("/api/analyze_name/{name}")
def analyze_name_get(name: str):
    try:
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        result = analyze_name(name.strip())
        logger.info(f"Successfully analyzed name: {name}")
        return result
    except Exception as e:
        logger.error(f"Error analyzing name '{name}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during name analysis")


# Pydantic Models
class NameIn(BaseModel):
    """Name analysis request model."""
    name: str = Field(..., min_length=1, description="Name to analyze")


# Pydantic Models for Panchangam API
class LocationInfo(BaseModel):
    """Location information for panchangam calculations."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    timezone: str = Field(default="Asia/Kolkata", description="Timezone string")


class TithiInfo(BaseModel):
    """Tithi (lunar day) information."""
    number: int = Field(..., ge=1, le=30, description="Tithi number (1-30)")
    name: str = Field(..., description="Tithi name (e.g., 'Shukla 1', 'Krishna 15')")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progress within tithi (0.0-1.0)")
    percentage: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")


class NakshatraInfo(BaseModel):
    """Nakshatra (lunar mansion) information."""
    number: int = Field(..., ge=1, le=27, description="Nakshatra number (1-27)")
    name: str = Field(..., description="Nakshatra name")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progress within nakshatra (0.0-1.0)")
    percentage: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")


class YogaInfo(BaseModel):
    """Yoga information."""
    number: int = Field(..., ge=1, le=27, description="Yoga number (1-27)")
    name: str = Field(..., description="Yoga name")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progress within yoga (0.0-1.0)")
    percentage: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")


class KaranaInfo(BaseModel):
    """Karana information."""
    name: str = Field(..., description="Karana name")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progress within karana (0.0-1.0)")
    percentage: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")


class TimePeriod(BaseModel):
    """Time period information."""
    start: str = Field(..., description="Start time in ISO format")
    end: str = Field(..., description="End time in ISO format")
    duration_hours: float = Field(..., description="Duration in hours")


class HoraInfo(BaseModel):
    """Hora (planetary hour) information."""
    hora_number: int = Field(..., ge=1, le=12, description="Hora number (1-12)")
    planet: str = Field(..., description="Ruling planet")
    start: str = Field(..., description="Start time in ISO format")
    end: str = Field(..., description="End time in ISO format")


class GowriPeriods(BaseModel):
    """Gowri Panchangam periods."""
    amrutha: TimePeriod
    siddha: TimePeriod
    marana: TimePeriod
    rogam: TimePeriod
    laabha: TimePeriod
    dhanam: TimePeriod
    sugam: TimePeriod
    kantaka: TimePeriod


class GowriInfo(BaseModel):
    """Gowri Panchangam information."""
    periods: GowriPeriods
    auspicious: List[str] = Field(..., description="List of auspicious period names")
    inauspicious: List[str] = Field(..., description="List of inauspicious period names")


class PanchangamResponse(BaseModel):
    """Complete panchangam response."""
    date: str = Field(..., description="Date in ISO format")
    location: LocationInfo
    sunrise: str = Field(..., description="Sunrise time in ISO format")
    sunset: str = Field(..., description="Sunset time in ISO format")
    tithi: TithiInfo
    nakshatra: NakshatraInfo
    yoga: YogaInfo
    karana: KaranaInfo
    rahu_kalam: TimePeriod
    yama_gandam: TimePeriod
    gulikai_kalam: TimePeriod
    horas: List[HoraInfo]
    gowri_panchangam: GowriInfo
    settings: Optional[Dict[str, Any]] = Field(default=None, description="Calculation settings")


class PanchangamRequest(BaseModel):
    """Panchangam calculation request."""
    date: date = Field(..., description="Date for panchangam calculation")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    timezone: str = Field(default="Asia/Kolkata", description="Timezone string")
    settings: Optional[Dict[str, Any]] = Field(default=None, description="Additional settings")


# Initialize Redis cache
@app.on_event("startup")
async def startup():
    """Initialize Redis cache on startup."""
    if settings.REDIS_URL:
        try:
            redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
            FastAPICache.init(RedisBackend(redis_client), prefix="panchangam-cache")
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {str(e)}")
            logger.info("Continuing without cache")
    else:
        logger.info("No Redis URL provided, running without cache")


# Panchangam Routes
@app.get("/api/panchangam/{date}", response_model=PanchangamResponse)
@cache(expire=3600)  # Cache for 1 hour
async def get_panchangam(
    date: date = Path(..., description="Date for panchangam calculation (YYYY-MM-DD)"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query(default="Asia/Kolkata", description="Timezone string")
):
    """
    Get panchangam for a specific date and location.
    
    Args:
        date: Date for calculation (YYYY-MM-DD)
        lat: Latitude in degrees (-90 to 90)
        lon: Longitude in degrees (-180 to 180)
        tz: Timezone string (default: Asia/Kolkata)
    
    Returns:
        Complete panchangam information including tithi, nakshatra, yoga, karana,
        timing periods, horas, and Gowri panchangam.
    """
    try:
        logger.info(f"Calculating panchangam for {date} at ({lat}, {lon}) in {tz}")
        
        # Assemble panchangam
        panchangam_data = assemble_panchangam(date, lat, lon, tz)
        
        # Convert to response model
        response = PanchangamResponse(**panchangam_data)
        
        logger.info(f"Successfully calculated panchangam for {date}")
        return response
        
    except Exception as e:
        logger.error(f"Error calculating panchangam for {date}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during panchangam calculation")


@app.get("/api/calendar/{year}/{month}")
@cache(expire=7200)  # Cache for 2 hours
async def get_calendar_month(
    year: int = Path(..., ge=1900, le=2100, description="Year"),
    month: int = Path(..., ge=1, le=12, description="Month (1-12)"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query(default="Asia/Kolkata", description="Timezone string")
):
    """
    Get panchangam calendar for a specific month.
    
    Args:
        year: Year (1900-2100)
        month: Month (1-12)
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz: Timezone string
    
    Returns:
        List of panchangam data for each day in the month.
    """
    try:
        logger.info(f"Generating calendar for {year}-{month:02d} at ({lat}, {lon})")
        
        # Generate dates for the month
        from calendar import monthrange
        days_in_month = monthrange(year, month)[1]
        
        calendar_data = []
        for day in range(1, days_in_month + 1):
            date_obj = date(year, month, day)
            panchangam_data = assemble_panchangam(date_obj, lat, lon, tz)
            calendar_data.append(panchangam_data)
        
        logger.info(f"Successfully generated calendar for {year}-{month:02d}")
        return {
            "year": year,
            "month": month,
            "location": {"latitude": lat, "longitude": lon, "timezone": tz},
            "days": calendar_data
        }
        
    except Exception as e:
        logger.error(f"Error generating calendar for {year}-{month}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during calendar generation")


@app.get("/api/festivals")
@cache(expire=86400)  # Cache for 24 hours
async def get_festivals(
    year: int = Query(..., ge=1900, le=2100, description="Year"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Month (1-12), optional"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query(default="Asia/Kolkata", description="Timezone string"),
    region: str = Query(default="ALL", description="Region code (ALL, TN, KL, KA, AP, etc.)")
):
    """
    Get festivals and important dates for a year or month.
    
    Args:
        year: Year (1900-2100)
        month: Month (1-12), optional
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz: Timezone string
        region: Region code for regional festivals
    
    Returns:
        List of festivals and important dates.
    """
    try:
        logger.info(f"Getting festivals for {year}" + (f"-{month:02d}" if month else "") + f" in region {region}")
        
        if month:
            # Get festivals for specific month
            festivals = festival_service.build_month(year, month, lat, lon, tz, region)
        else:
            # Get festivals for entire year
            all_festivals = []
            for m in range(1, 13):
                month_festivals = festival_service.build_month(year, m, lat, lon, tz, region)
                all_festivals.extend(month_festivals)
            festivals = all_festivals
        
        logger.info(f"Successfully retrieved {len(festivals)} festivals for {year}")
        return {
            "year": year,
            "month": month,
            "region": region,
            "location": {"latitude": lat, "longitude": lon, "timezone": tz},
            "festivals": festivals,
            "total_count": len(festivals)
        }
        
    except Exception as e:
        logger.error(f"Error getting festivals for {year}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during festival retrieval")


@app.get("/api/muhurtham")
@cache(expire=3600)  # Cache for 1 hour
async def get_muhurtham(
    date: date = Query(..., description="Date for muhurtham calculation (YYYY-MM-DD)"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query(default="Asia/Kolkata", description="Timezone string"),
    event_type: str = Query(default="general", description="Type of event (marriage, house_warming, business_opening, vehicle_purchase, general)")
):
    """
    Get auspicious times (muhurtham) for a specific date and event.
    
    Args:
        date: Date for muhurtham calculation
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz: Timezone string
        event_type: Type of event (marriage, house_warming, business_opening, vehicle_purchase, general)
    
    Returns:
        List of auspicious time periods for the event.
    """
    try:
        logger.info(f"Calculating muhurtham for {date}, event: {event_type}")
        
        # Get muhurtham periods using festival service
        muhurtham_periods = festival_service.build_muhurtham_periods(
            date, lat, lon, tz, event_type
        )
        
        # Get panchangam data for additional context
        panchangam_data = assemble_panchangam(date, lat, lon, tz)
        
        logger.info(f"Successfully calculated {len(muhurtham_periods)} muhurtham periods for {date}")
        return {
            "date": date.isoformat(),
            "event_type": event_type,
            "location": {"latitude": lat, "longitude": lon, "timezone": tz},
            "auspicious_periods": muhurtham_periods,
            "panchangam_context": {
                "tithi": panchangam_data.get("tithi", {}),
                "nakshatra": panchangam_data.get("nakshatra", {}),
                "yoga": panchangam_data.get("yoga", {}),
                "karana": panchangam_data.get("karana", {}),
                "gowri_panchangam": panchangam_data.get("gowri_panchangam", {})
            },
            "total_periods": len(muhurtham_periods)
        }
        
    except Exception as e:
        logger.error(f"Error calculating muhurtham for {date}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during muhurtham calculation")
