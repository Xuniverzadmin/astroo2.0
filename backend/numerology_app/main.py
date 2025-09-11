from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base, check_database_connection
from .migrations.initial_schema import create_initial_schema
from .jobs import initialize_jobs, cleanup_jobs
from .config import settings

# Import routers
from .api_chat import router as chat_router
from .api_store import router as store_router
from .api_astro import router as astro_router
from .api_llm import router as llm_router
from .api_auth import router as auth_router
from .api_profiles import router as profiles_router
from .api_calendar import router as calendar_router
from .api_billing import router as billing_router
from .api_panchangam import router as panchangam_router
from .api_quick_reading import router as quick_reading_router
from .api_birth_chart import router as birth_chart_router
from .api_dasha import router as dasha_router
from .api_events import router as events_router
from .api_interpretation import router as interpretation_router


app = FastAPI(title="Astrooverz API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize database and create tables on startup."""
    try:
        # Check database connection
        if not check_database_connection():
            raise Exception("Database connection failed during startup")
        
        # Create initial schema
        create_initial_schema()
        
        # Initialize job system if enabled and in production
        if settings.SCHED_ENABLED:
            await initialize_jobs()
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Startup failed: {str(e)}")
        # Don't raise here to allow the app to start even if some services are unavailable


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Cleanup resources on shutdown."""
    try:
        if settings.SCHED_ENABLED:
            await cleanup_jobs()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Shutdown cleanup failed: {str(e)}")


# Mount all API routers under /api
for router in (
    chat_router,
    store_router,
    astro_router,
    llm_router,
    auth_router,
    profiles_router,
    calendar_router,
    billing_router,
    panchangam_router,
    quick_reading_router,
    birth_chart_router,
    dasha_router,
    events_router,
    interpretation_router,
):
    app.include_router(router, prefix="/api")


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}

@app.get("/api/healthz")
def api_healthz() -> dict[str, str | bool]:
    return {"ok": True, "status": "healthy", "service": "numerology-api"}

# Quick reading endpoint (temporary direct implementation)
from pydantic import BaseModel
from datetime import datetime

class QuickReadingRequest(BaseModel):
    name: str
    dob: str
    time_of_birth: str
    location: str

class QuickReadingResponse(BaseModel):
    name: str
    birth_details: dict
    numerology: dict
    panchangam: dict
    guidance: str
    auspicious_times: list
    message: str

@app.post("/api/quick-reading", response_model=QuickReadingResponse)
async def quick_reading(request: QuickReadingRequest):
    """Generate a quick Vedic astrology reading based on birth details."""
    try:
        # Parse birth date and time
        birth_date = datetime.strptime(request.dob, "%Y-%m-%d").date()
        birth_time = datetime.strptime(request.time_of_birth, "%H:%M").time()
        
        # Calculate numerology (simplified version)
        name_number = calculate_name_number(request.name)
        birth_number = calculate_birth_number(birth_date)
        life_path_number = calculate_life_path_number(birth_date)
        
        return QuickReadingResponse(
            name=request.name,
            birth_details={
                "date_of_birth": request.dob,
                "time_of_birth": request.time_of_birth,
                "location": request.location,
                "timezone": "Auto-detected"
            },
            numerology={
                "name_number": name_number,
                "birth_number": birth_number,
                "life_path_number": life_path_number,
                "ruling_planet": get_ruling_planet(name_number),
                "personality_traits": get_personality_traits(name_number)
            },
            panchangam={
                "birth_nakshatra": "Based on your birth details, your nakshatra influences your personality and life path.",
                "auspicious_days": ["Monday", "Wednesday", "Friday"],
                "favorable_colors": ["Red", "Orange", "Gold"],
                "lucky_numbers": [1, 3, 7],
                "recommended_gems": ["Ruby", "Red Coral", "Diamond"]
            },
            guidance=generate_vedic_guidance(name_number, birth_number, life_path_number),
            auspicious_times=[
                "Early morning (6:00 AM - 8:00 AM) - Best for spiritual practices",
                "Mid-morning (10:00 AM - 12:00 PM) - Ideal for important decisions",
                "Evening (6:00 PM - 8:00 PM) - Good for family and relationships",
                "Late evening (8:00 PM - 10:00 PM) - Perfect for planning and reflection"
            ],
            message="This is a simplified reading. For detailed analysis, please consult with our full astrology service."
        )
        
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Invalid date or time format: {str(e)}")
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Error generating reading. Please try again.")

def calculate_name_number(name: str) -> int:
    """Calculate numerology number from name using Vedic system"""
    clean_name = name.replace(" ", "").upper()
    vedic_mapping = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'K': 2, 'R': 2,
        'C': 3, 'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5, 'X': 5,
        'U': 6, 'V': 6, 'W': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    total = 0
    for char in clean_name:
        if char in vedic_mapping:
            total += vedic_mapping[char]
    while total > 9:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_birth_number(birth_date) -> int:
    """Calculate birth number from date"""
    day = birth_date.day
    while day > 9:
        day = sum(int(digit) for digit in str(day))
    return day

def calculate_life_path_number(birth_date) -> int:
    """Calculate life path number from full birth date"""
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(digit) for digit in date_str)
    while total > 9:
        total = sum(int(digit) for digit in str(total))
    return total

def get_ruling_planet(number: int) -> str:
    """Get ruling planet based on numerology number"""
    planets = {
        1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 
        5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"
    }
    return planets.get(number, "Unknown")

def get_personality_traits(number: int) -> list:
    """Get personality traits based on numerology number"""
    traits = {
        1: ["Leadership", "Independence", "Originality", "Determination"],
        2: ["Cooperation", "Diplomacy", "Intuition", "Patience"],
        3: ["Creativity", "Optimism", "Communication", "Joy"],
        4: ["Practicality", "Organization", "Stability", "Hard work"],
        5: ["Freedom", "Adventure", "Versatility", "Curiosity"],
        6: ["Responsibility", "Nurturing", "Harmony", "Service"],
        7: ["Spirituality", "Analysis", "Perfectionism", "Wisdom"],
        8: ["Ambition", "Material success", "Authority", "Efficiency"],
        9: ["Humanitarianism", "Compassion", "Generosity", "Universal love"]
    }
    return traits.get(number, ["Unique personality"])

def generate_vedic_guidance(name_number: int, birth_number: int, life_path_number: int):
    """Generate Vedic guidance based on numerology"""
    guidance_templates = {
        1: "As a number 1, you are a natural leader. Focus on your independence and originality. The Sun's energy guides you to shine brightly in your endeavors.",
        2: "Your number 2 nature brings cooperation and diplomacy. Trust your intuition and work harmoniously with others. The Moon's influence helps you connect with emotions.",
        3: "Creativity and joy flow through you as a number 3. Express yourself freely and spread optimism. Jupiter's wisdom guides your communication.",
        4: "Your practical nature as a number 4 brings stability. Focus on organization and hard work. Rahu's energy helps you build solid foundations.",
        5: "Freedom and adventure define your number 5 nature. Embrace change and seek new experiences. Mercury's versatility guides your path.",
        6: "Responsibility and nurturing come naturally to you as a number 6. Focus on service and harmony. Venus's love energy surrounds you.",
        7: "Your spiritual nature as a number 7 seeks deeper meaning. Trust your analytical mind and inner wisdom. Ketu's mystical energy guides you.",
        8: "Material success and authority are your number 8 gifts. Focus on your ambitions with integrity. Saturn's discipline strengthens your resolve.",
        9: "Your humanitarian nature as a number 9 brings compassion. Serve others and spread universal love. Mars's energy drives your noble causes."
    }
    primary_number = name_number
    return guidance_templates.get(primary_number, "Your unique path combines ancient wisdom with modern possibilities.")
