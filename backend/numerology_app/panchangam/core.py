"""
Core panchangam computation functions.

This module contains the main algorithms for calculating Vedic panchangam elements
including tithi, nakshatra, yoga, karana, and other astrological timings.
"""

import math
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional, Any
import pytz

from .astronomy import get_sun_longitude, get_moon_longitude, get_sunrise_sunset, sunrise_sunset_local, sun_moon_ecliptic_longitudes


# Constants for panchangam calculations
LAHIRI_AYANAMSA = 50.2388475  # Degrees for 2000.0 epoch
TITHI_DURATION = 12.0  # Degrees (360/30 tithis)
NAKSHATRA_DURATION = 13.333333  # Degrees (360/27 nakshatras)
YOGAS = [
    "Vishkambha", "Preeti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

KARANAS = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti",
    "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]


def compute_tithi(sun_long: float, moon_long: float) -> Tuple[int, float]:
    """
    Calculate tithi (lunar day) from sun and moon longitudes.
    
    Args:
        sun_long: Sun's sidereal longitude in degrees
        moon_long: Moon's sidereal longitude in degrees
        
    Returns:
        Tuple of (tithi_number, tithi_progress)
        - tithi_number: 1-30 (1=Shukla Pratipada, 16=Krishna Pratipada)
        - tithi_progress: 0.0-1.0 (progress within the tithi)
        
    Formula:
        tithi = (moon_long - sun_long) / 12.0
        If tithi < 0, add 30
        tithi_number = floor(tithi) + 1
        tithi_progress = tithi - floor(tithi)
    """
    # Calculate tithi difference
    tithi_diff = (moon_long - sun_long) % 360
    
    # Convert to tithi number (0-29)
    tithi_raw = tithi_diff / TITHI_DURATION
    
    # Get tithi number (1-30)
    tithi_number = int(tithi_raw) + 1
    
    # Get progress within tithi (0.0-1.0)
    tithi_progress = tithi_raw - int(tithi_raw)
    
    return tithi_number, tithi_progress


def compute_nakshatra(moon_long: float) -> Tuple[int, float]:
    """
    Calculate nakshatra (lunar mansion) from moon longitude.
    
    Args:
        moon_long: Moon's sidereal longitude in degrees
        
    Returns:
        Tuple of (nakshatra_number, nakshatra_progress)
        - nakshatra_number: 1-27
        - nakshatra_progress: 0.0-1.0 (progress within the nakshatra)
        
    Formula:
        nakshatra = moon_long / 13.333333
        nakshatra_number = floor(nakshatra) + 1
        nakshatra_progress = nakshatra - floor(nakshatra)
    """
    # Calculate nakshatra number (0-26)
    nakshatra_raw = moon_long / NAKSHATRA_DURATION
    
    # Get nakshatra number (1-27)
    nakshatra_number = int(nakshatra_raw) + 1
    
    # Get progress within nakshatra (0.0-1.0)
    nakshatra_progress = nakshatra_raw - int(nakshatra_raw)
    
    return nakshatra_number, nakshatra_progress


def compute_yoga(sun_long: float, moon_long: float) -> Tuple[int, float]:
    """
    Calculate yoga from sun and moon longitudes.
    
    Args:
        sun_long: Sun's sidereal longitude in degrees
        moon_long: Moon's sidereal longitude in degrees
        
    Returns:
        Tuple of (yoga_number, yoga_progress)
        - yoga_number: 1-27
        - yoga_progress: 0.0-1.0 (progress within the yoga)
        
    Formula:
        yoga_sum = (sun_long + moon_long) % 360
        yoga = yoga_sum / 13.333333
        yoga_number = floor(yoga) + 1
        yoga_progress = yoga - floor(yoga)
    """
    # Calculate yoga sum
    yoga_sum = (sun_long + moon_long) % 360
    
    # Calculate yoga number (0-26)
    yoga_raw = yoga_sum / NAKSHATRA_DURATION  # Same duration as nakshatra
    
    # Get yoga number (1-27)
    yoga_number = int(yoga_raw) + 1
    
    # Get progress within yoga (0.0-1.0)
    yoga_progress = yoga_raw - int(yoga_raw)
    
    return yoga_number, yoga_progress


def compute_karana(tithi_number: int, tithi_progress: float) -> Tuple[str, float]:
    """
    Calculate karana from tithi information.
    
    Args:
        tithi_number: Tithi number (1-30)
        tithi_progress: Progress within tithi (0.0-1.0)
        
    Returns:
        Tuple of (karana_name, karana_progress)
        - karana_name: Name of the karana
        - karana_progress: 0.0-1.0 (progress within the karana)
        
    Formula:
        - Each tithi has 2 karanas
        - First 7 karanas repeat in cycle
        - 8th karana (Vishti) occurs only once per tithi
        - Karanas 9-11 occur only on specific tithis
    """
    # Calculate karana index (0-10)
    karana_index = int(tithi_progress * 2)  # 2 karanas per tithi
    
    # Handle special karanas
    if tithi_number in [1, 6, 11, 16, 21, 26]:  # Specific tithis for karanas 9-11
        if karana_index == 0:
            karana_name = KARANAS[8]  # Chatushpada
        else:
            karana_name = KARANAS[9]  # Naga
    elif tithi_number in [2, 7, 12, 17, 22, 27]:
        if karana_index == 0:
            karana_name = KARANAS[9]  # Naga
        else:
            karana_name = KARANAS[10]  # Kimstughna
    else:
        # Regular karanas (0-6 cycle)
        karana_name = KARANAS[karana_index % 7]
    
    # Calculate progress within karana
    karana_progress = (tithi_progress * 2) - karana_index
    
    return karana_name, karana_progress


def compute_rahu_yama_gulikai(date_obj: date, lat: float, lon: float, tz: str) -> Dict[str, Any]:
    """
    Calculate Rahu Kalam, Yama Gandam, and Gulikai Kalam.
    
    Args:
        date_obj: Date for calculation
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz: Timezone string
        
    Returns:
        Dictionary with timing information
        
    Formula:
        - Rahu Kalam: 1.5 hours, varies by weekday
        - Yama Gandam: 1.5 hours, varies by weekday  
        - Gulikai Kalam: 1.5 hours, varies by weekday
        - Times are calculated from sunrise
    """
    # Get sunrise and sunset
    sunrise, sunset = get_sunrise_sunset(date_obj, lat, lon, tz)
    
    # Calculate day duration
    day_duration = sunset - sunrise
    day_hours = day_duration.total_seconds() / 3600
    
    # Get weekday (0=Monday, 6=Sunday)
    weekday = date_obj.weekday()
    
    # Rahu Kalam periods (1.5 hours each)
    rahu_periods = [
        (8, 9.5),   # Monday
        (3, 4.5),   # Tuesday
        (12, 13.5), # Wednesday
        (1.5, 3),   # Thursday
        (10.5, 12), # Friday
        (9, 10.5),  # Saturday
        (4.5, 6)    # Sunday
    ]
    
    # Yama Gandam periods
    yama_periods = [
        (3, 4.5),   # Monday
        (12, 13.5), # Tuesday
        (1.5, 3),   # Wednesday
        (10.5, 12), # Thursday
        (9, 10.5),  # Friday
        (4.5, 6),   # Saturday
        (8, 9.5)    # Sunday
    ]
    
    # Gulikai Kalam periods
    gulikai_periods = [
        (12, 13.5), # Monday
        (1.5, 3),   # Tuesday
        (10.5, 12), # Wednesday
        (9, 10.5),  # Thursday
        (4.5, 6),   # Friday
        (8, 9.5),   # Saturday
        (3, 4.5)    # Sunday
    ]
    
    # Calculate actual times
    def get_time_from_period(start_hour, end_hour):
        start_time = sunrise + timedelta(hours=start_hour)
        end_time = sunrise + timedelta(hours=end_hour)
        return start_time, end_time
    
    rahu_start, rahu_end = get_time_from_period(*rahu_periods[weekday])
    yama_start, yama_end = get_time_from_period(*yama_periods[weekday])
    gulikai_start, gulikai_end = get_time_from_period(*gulikai_periods[weekday])
    
    return {
        "rahu_kalam": {
            "start": rahu_start,
            "end": rahu_end,
            "duration_hours": 1.5
        },
        "yama_gandam": {
            "start": yama_start,
            "end": yama_end,
            "duration_hours": 1.5
        },
        "gulikai_kalam": {
            "start": gulikai_start,
            "end": gulikai_end,
            "duration_hours": 1.5
        }
    }


def compute_hora(date_obj: date, lat: float, lon: float, tz: str) -> List[Dict[str, Any]]:
    """
    Calculate Hora (planetary hours) for the day.
    
    Args:
        date_obj: Date for calculation
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz: Timezone string
        
    Returns:
        List of hora periods with planetary rulers
        
    Formula:
        - Day divided into 12 horas
        - Each hora ruled by a planet in sequence
        - Sequence: Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars
        - Repeats for 12 horas
    """
    sunrise, sunset = get_sunrise_sunset(date_obj, lat, lon, tz)
    
    # Calculate day duration
    day_duration = sunset - sunrise
    hora_duration = day_duration / 12
    
    # Planetary sequence
    planets = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    
    horas = []
    current_time = sunrise
    
    for i in range(12):
        planet = planets[i % 7]
        start_time = current_time
        end_time = current_time + hora_duration
        
        horas.append({
            "hora_number": i + 1,
            "planet": planet,
            "start": start_time,
            "end": end_time,
            "duration": hora_duration
        })
        
        current_time = end_time
    
    return horas


def compute_gowri_nalla(date_obj: date, lat: float, lon: float, tz: str) -> Dict[str, Any]:
    """
    Calculate Gowri Panchangam (auspicious times).
    
    Args:
        date_obj: Date for calculation
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz: Timezone string
        
    Returns:
        Dictionary with Gowri timings
        
    Formula:
        - Based on tithi and nakshatra
        - Different periods for different activities
        - Auspicious and inauspicious times
    """
    # Get sunrise and sunset
    sunrise, sunset = get_sunrise_sunset(date_obj, lat, lon, tz)
    
    # Calculate day duration
    day_duration = sunset - sunrise
    day_hours = day_duration.total_seconds() / 3600
    
    # Gowri periods (approximate, varies by location and tradition)
    gowri_periods = {
        "amrutha": (sunrise + timedelta(hours=6), sunrise + timedelta(hours=7.5)),
        "siddha": (sunrise + timedelta(hours=7.5), sunrise + timedelta(hours=9)),
        "marana": (sunrise + timedelta(hours=9), sunrise + timedelta(hours=10.5)),
        "rogam": (sunrise + timedelta(hours=10.5), sunrise + timedelta(hours=12)),
        "laabha": (sunrise + timedelta(hours=12), sunrise + timedelta(hours=13.5)),
        "dhanam": (sunrise + timedelta(hours=13.5), sunrise + timedelta(hours=15)),
        "sugam": (sunrise + timedelta(hours=15), sunrise + timedelta(hours=16.5)),
        "kantaka": (sunrise + timedelta(hours=16.5), sunrise + timedelta(hours=18))
    }
    
    return {
        "periods": gowri_periods,
        "auspicious": ["amrutha", "siddha", "laabha", "dhanam", "sugam"],
        "inauspicious": ["marana", "rogam", "kantaka"]
    }


def assemble_panchangam(date_obj: date, lat: float, lon: float, tz: str, 
                       settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Assemble complete panchangam for a given date and location.
    
    Args:
        date_obj: Date for calculation
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz: Timezone string
        settings: Optional settings dictionary
        
    Returns:
        Complete panchangam dictionary with all calculated elements
        
    Formula:
        Combines all panchangam elements:
        - Tithi, Nakshatra, Yoga, Karana
        - Sunrise/Sunset times
        - Rahu Kalam, Yama Gandam, Gulikai Kalam
        - Hora periods
        - Gowri Panchangam
    """
    if settings is None:
        settings = {}
    
    # Get sunrise and sunset using modern API
    sunrise_iso, sunset_iso = sunrise_sunset_local(date_obj.isoformat(), lat, lon, tz)
    
    # Calculate sun and moon positions at local noon for day-level calculations
    import zoneinfo
    local_noon = datetime.fromisoformat(f"{date_obj.isoformat()}T12:00:00").replace(tzinfo=zoneinfo.ZoneInfo(tz))
    sun_long, moon_long = sun_moon_ecliptic_longitudes(local_noon, lat, lon)
    
    # Calculate panchangam elements
    tithi_num, tithi_progress = compute_tithi(sun_long, moon_long)
    nakshatra_num, nakshatra_progress = compute_nakshatra(moon_long)
    yoga_num, yoga_progress = compute_yoga(sun_long, moon_long)
    karana_name, karana_progress = compute_karana(tithi_num, tithi_progress)
    
    # Calculate timing elements
    rahu_yama_gulikai = compute_rahu_yama_gulikai(date_obj, lat, lon, tz)
    horas = compute_hora(date_obj, lat, lon, tz)
    gowri = compute_gowri_nalla(date_obj, lat, lon, tz)
    
    # Determine tithi name
    if tithi_num <= 15:
        tithi_name = f"Shukla {tithi_num}"
    else:
        tithi_name = f"Krishna {tithi_num - 15}"
    
    return {
        "date": date_obj.isoformat(),
        "location": {
            "latitude": lat,
            "longitude": lon,
            "timezone": tz
        },
        "sunrise": sunrise_iso,
        "sunset": sunset_iso,
        "tithi": {
            "number": tithi_num,
            "name": tithi_name,
            "progress": tithi_progress,
            "percentage": round(tithi_progress * 100, 2)
        },
        "nakshatra": {
            "number": nakshatra_num,
            "name": NAKSHATRAS[nakshatra_num - 1],
            "progress": nakshatra_progress,
            "percentage": round(nakshatra_progress * 100, 2)
        },
        "yoga": {
            "number": yoga_num,
            "name": YOGAS[yoga_num - 1],
            "progress": yoga_progress,
            "percentage": round(yoga_progress * 100, 2)
        },
        "karana": {
            "name": karana_name,
            "progress": karana_progress,
            "percentage": round(karana_progress * 100, 2)
        },
        "rahu_kalam": rahu_yama_gulikai["rahu_kalam"],
        "yama_gandam": rahu_yama_gulikai["yama_gandam"],
        "gulikai_kalam": rahu_yama_gulikai["gulikai_kalam"],
        "horas": [
            {
                "hora_number": h["hora_number"],
                "planet": h["planet"],
                "start": h["start"].isoformat(),
                "end": h["end"].isoformat()
            }
            for h in horas
        ],
        "gowri_panchangam": gowri,
        "settings": settings
    }


# TODO: Add unit tests for:
# - compute_tithi() with known sun/moon positions
# - compute_nakshatra() with known moon positions
# - compute_yoga() with known sun/moon positions
# - compute_karana() with known tithi values
# - compute_rahu_yama_gulikai() with known dates
# - compute_hora() with known dates
# - compute_gowri_nalla() with known dates
# - assemble_panchangam() integration tests
# - Edge cases: leap years, timezone boundaries, polar regions
# - Accuracy validation against published panchangam data
