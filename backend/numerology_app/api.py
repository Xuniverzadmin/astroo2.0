from fastapi import APIRouter, HTTPException, Query, Path, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import logging
import os
from .panchangam_utils import compute_windows, format_window

# --- Caching imports (with safe fallback for editors/local) ---
try:
    from fastapi_cache import FastAPICache  # type: ignore
    from fastapi_cache.backends.redis import RedisBackend  # type: ignore
    from fastapi_cache.decorator import cache  # type: ignore
    import redis.asyncio as redis  # type: ignore
    _CACHE_OK = True
except Exception:
    _CACHE_OK = False
    def cache(*_args, **_kw):
        # no-op decorator when cache libs aren't installed/available
        def _wrap(fn):
            return fn
        return _wrap

from .core_utils import analyze_name
from .panchangam.core import assemble_panchangam
from .festivals.service import festival_service
from .config import settings
from .llm import ask_one_shot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models
class NameIn(BaseModel):
    """Name analysis request model."""
    name: str = Field(..., min_length=1, description="Name to analyze")

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MiniReadingInput(BaseModel):
    name: str
    dob: str  # ISO date "YYYY-MM-DD"
    tob: Optional[str] = None  # "HH:MM"
    location: Optional[str] = None  # "City, Country" or lat,long

class MiniReadingOutput(BaseModel):
    summary: str

class AskInput(BaseModel):
    question: str
    profile_id: Optional[str] = None
    # Optional quick geo; later you can resolve from user profile
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None  # default Asia/Kolkata

class AskOutput(BaseModel):
    answer: str

router = APIRouter()

# Router is ready - middleware will be handled in main.py

@router.get("/")
def root():
    return {"message": "Astrooverz Numerology API", "status": "running"}

@router.get("/healthz")
def healthz():
    return {"ok": True, "status": "healthy", "service": "numerology-api"}

@router.post("/auth/login", response_model=LoginResponse)
def login(req: LoginRequest):
    """Login endpoint for user authentication."""
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail="Missing credentials")
    # TODO: replace with real auth
    return {"access_token": "demo-token", "token_type": "bearer"}

@router.post("/readings/mini", response_model=MiniReadingOutput)
@cache(expire=120)  # cache identical inputs for 2 minutes
def mini_reading(payload: MiniReadingInput):
    """
    Return a natural-language short summary only.
    The UI will render summary as plain text.
    """
    # TODO: call your real calculators here (numerology + panchangam)
    # Keep the API contract minimal and stable:
    text = (
        f"Hi {payload.name}, based on your details "
        f"({payload.dob}{' ' + payload.tob if payload.tob else ''}"
        f"{', ' + payload.location if payload.location else ''}), "
        "today favors focused tasks over new beginnings. "
        "Best time window: 10:30–12:00. Avoid major commitments during Rahu Kalam. "
        "A quick win: finish one pending item and send a progress update."
    )
    return {"summary": text}

@router.post("/ask", response_model=AskOutput)
@cache(expire=60)  # cache short-lived answers for 1 minute
def ask_astrooverz(payload: AskInput):
    """
    LLM-backed answer with real Panchangam timings. Keep the response as a single answer string.
    """
    q = payload.question.strip()
    if not q:
        return {"answer": "Please ask a question."}
    
    try:
        # --- Panchangam context (defaults to Chennai if coords not provided) ---
        lat = payload.lat if payload.lat is not None else 13.0827
        lon = payload.lon if payload.lon is not None else 80.2707
        tz  = payload.tz  if payload.tz  else "Asia/Kolkata"
        w = compute_windows(date.today(), lat=lat, lon=lon, tz=tz)

        # Build a concise context string
        ctx_lines = [
            f"Sunrise {w.sunrise.strftime('%H:%M')}, Sunset {w.sunset.strftime('%H:%M')} ({tz})",
            f"Rahu Kalam: {format_window(w.rahu)}",
            f"Yamaganda: {format_window(w.yamaganda)}",
            f"Gulikai: {format_window(w.gulikai)}",
            "Good windows (avoid the above): " + ", ".join(format_window(b) for b in w.best_windows[:3]) + (" …" if len(w.best_windows) > 3 else "")
        ]
        panchangam_context = "\n".join(ctx_lines)

        # Prompt the LLM with real timings
        prompt = (
            "You are a concise, practical Vedic astrology guide. "
            "Use the provided Panchangam timings exactly—do not invent times.\n\n"
            f"PANCHANGAM TODAY (local):\n{panchangam_context}\n\n"
            f"USER QUESTION:\n{q}\n\n"
            "Answer in 3-5 bullet points max. If the user asks for an auspicious time, "
            "recommend a BEST WINDOW that does not overlap Rahu, Yamaganda, or Gulikai, "
            "and mention one practical action."
        )

        ans = ask_one_shot(prompt)
        if not ans:
            return {"answer": "I couldn't generate a reply.", "error": "empty_completion"}
        return {"answer": ans}
    except Exception as e:
        logger.error(f"Error in ask_astrooverz: {e}")
        return {"answer": f"Sorry, I encountered an error: {str(e)}"}

@router.get("/diag/panchangam")
def diag_panchangam(lat: float = 13.0827, lon: float = 80.2707, tz: str = "Asia/Kolkata"):
    """Diagnostic endpoint to verify Panchangam calculations."""
    try:
        w = compute_windows(date.today(), lat=lat, lon=lon, tz=tz)
        return {
            "sunrise": w.sunrise.isoformat(),
            "sunset": w.sunset.isoformat(),
            "rahu": format_window(w.rahu),
            "yamaganda": format_window(w.yamaganda),
            "gulikai": format_window(w.gulikai),
            "best_windows": [format_window(b) for b in w.best_windows],
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/analyze_name")
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

@router.get("/analyze_name/{name}")
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
    target_date: date = Field(..., description="Date for panchangam calculation")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    timezone: str = Field(default="Asia/Kolkata", description="Timezone string")
    settings: Optional[Dict[str, Any]] = Field(default=None, description="Additional settings")


@router.on_event("startup")
async def _init_cache():
    """Initialize Redis cache on startup with safe fallback."""
    if _CACHE_OK:
        try:
            url = os.getenv("REDIS_URL", "redis://redis:6379/0")
            r = redis.from_url(url, encoding="utf-8", decode_responses=True)
            FastAPICache.init(RedisBackend(r), prefix="astrooverz")
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {str(e)}")
            logger.info("Continuing without cache")
    else:
        logger.info("Cache libraries not available, running without cache")


# Panchangam Routes - Friendly API endpoints (ordered from most specific to least specific)
@router.get("/panchangam/today")
@cache(expire=3600)  # Cache for 1 hour
async def get_panchangam_today(
    lat: float = Query(13.0827, ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(80.2707, ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query("Asia/Kolkata", description="Timezone string"),
):
    """
    Get panchangam for today's date and location.
    
    Args:
        lat: Latitude in degrees (default: 13.0827 for Chennai)
        lon: Longitude in degrees (default: 80.2707 for Chennai)
        tz: Timezone string (default: Asia/Kolkata)
    
    Returns:
        Complete panchangam information for today.
    """
    try:
        today = datetime.now().date()
        logger.info(f"Calculating panchangam for today ({today}) at ({lat}, {lon}) in {tz}")
        return assemble_panchangam(today, lat, lon, tz, settings=None)
    except Exception as e:
        logger.error(f"Error calculating panchangam for today: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/panchangam/{date}")
@cache(expire=3600)  # Cache for 1 hour
async def get_panchangam_by_date(
    date: date = Path(..., description="Date for panchangam calculation (YYYY-MM-DD)"),
    lat: float = Query(13.0827, ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(80.2707, ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query("Asia/Kolkata", description="Timezone string"),
):
    """
    Get panchangam for a specific date and location.
    
    Args:
        date: Date for calculation (YYYY-MM-DD)
        lat: Latitude in degrees (default: 13.0827 for Chennai)
        lon: Longitude in degrees (default: 80.2707 for Chennai)
        tz: Timezone string (default: Asia/Kolkata)
    
    Returns:
        Complete panchangam information.
    """
    try:
        logger.info(f"Calculating panchangam for {date} at ({lat}, {lon}) in {tz}")
        
        # DEBUG: Check what assemble_panchangam returns
        result = assemble_panchangam(date, lat, lon, tz, settings=None)
        logger.info(f"Panchangam result type: {type(result)}")
        logger.info(f"Panchangam result: {result}")
        
        if not result:
            logger.error(f"assemble_panchangam returned None/empty for {date}")
            raise HTTPException(status_code=404, detail="Panchangam data not available")
        
        return result
    except Exception as e:
        logger.error(f"Error calculating panchangam for {date}: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/{year}/{month}")
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


@router.get("/festivals")
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


@router.get("/muhurtham")
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
