from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quick-reading", tags=["quick-reading"])

class QuickReadingRequest(BaseModel):
    name: str = Field(..., description="Full name of the person")
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    time_of_birth: str = Field(..., description="Time of birth in HH:MM format (24-hour)")
    location: str = Field(..., description="Birth location (City, Country)")
    timezone: Optional[str] = Field(None, description="Timezone (will be auto-detected if not provided)")

class QuickReadingResponse(BaseModel):
    name: str
    birth_details: dict
    numerology: dict
    panchangam: dict
    guidance: str
    auspicious_times: list
    message: str

@router.post("/", response_model=QuickReadingResponse)
async def quick_reading(request: QuickReadingRequest):
    """
    Generate a quick Vedic astrology reading based on birth details.
    This provides numerology, panchangam insights, and life guidance.
    """
    try:
        # Parse birth date and time
        birth_date = datetime.strptime(request.dob, "%Y-%m-%d").date()
        birth_time = datetime.strptime(request.time_of_birth, "%H:%M").time()
        
        # Calculate numerology (simplified version)
        name_number = calculate_name_number(request.name)
        birth_number = calculate_birth_number(birth_date)
        life_path_number = calculate_life_path_number(birth_date)
        
        # Generate panchangam insights (simplified)
        panchangam_insights = generate_panchangam_insights(birth_date, birth_time)
        
        # Generate guidance based on Vedic principles
        guidance = generate_vedic_guidance(name_number, birth_number, life_path_number)
        
        # Generate auspicious times
        auspicious_times = generate_auspicious_times(birth_date)
        
        return QuickReadingResponse(
            name=request.name,
            birth_details={
                "date_of_birth": request.dob,
                "time_of_birth": request.time_of_birth,
                "location": request.location,
                "timezone": request.timezone or "Auto-detected"
            },
            numerology={
                "name_number": name_number,
                "birth_number": birth_number,
                "life_path_number": life_path_number,
                "ruling_planet": get_ruling_planet(name_number),
                "personality_traits": get_personality_traits(name_number)
            },
            panchangam=panchangam_insights,
            guidance=guidance,
            auspicious_times=auspicious_times,
            message="This is a simplified reading. For detailed analysis, please consult with our full astrology service."
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date or time format: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating quick reading: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating reading. Please try again.")

def calculate_name_number(name: str) -> int:
    """Calculate numerology number from name using Vedic system"""
    # Remove spaces and convert to uppercase
    clean_name = name.replace(" ", "").upper()
    
    # Vedic numerology mapping
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
    
    # Reduce to single digit
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

def generate_panchangam_insights(birth_date, birth_time):
    """Generate simplified panchangam insights"""
    return {
        "birth_nakshatra": "Based on your birth details, your nakshatra influences your personality and life path.",
        "auspicious_days": ["Monday", "Wednesday", "Friday"],
        "favorable_colors": ["Red", "Orange", "Gold"],
        "lucky_numbers": [1, 3, 7],
        "recommended_gems": ["Ruby", "Red Coral", "Diamond"]
    }

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
    
    primary_number = name_number  # Use name number as primary
    return guidance_templates.get(primary_number, "Your unique path combines ancient wisdom with modern possibilities.")

def generate_auspicious_times(birth_date):
    """Generate auspicious times for the person"""
    return [
        "Early morning (6:00 AM - 8:00 AM) - Best for spiritual practices",
        "Mid-morning (10:00 AM - 12:00 PM) - Ideal for important decisions",
        "Evening (6:00 PM - 8:00 PM) - Good for family and relationships",
        "Late evening (8:00 PM - 10:00 PM) - Perfect for planning and reflection"
    ]
