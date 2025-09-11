# backend/numerology_app/vedic_charts.py
"""
Vedic chart calculations using Swiss Ephemeris.
Provides natal chart, divisional charts (Vargas), and chart analysis.
"""

import swisseph as swe
import math
from datetime import datetime, date, time
from typing import Dict, List, Tuple, Optional
import pytz
import logging

logger = logging.getLogger(__name__)

class VedicChart:
    """Main class for Vedic chart calculations."""
    
    # Planet constants
    SUN = swe.SUN
    MOON = swe.MOON
    MARS = swe.MARS
    MERCURY = swe.MERCURY
    JUPITER = swe.JUPITER
    VENUS = swe.VENUS
    SATURN = swe.SATURN
    RAHU = swe.MEAN_NODE  # North Node
    KETU = swe.MEAN_NODE  # South Node (180 degrees from Rahu)
    
    # Planet names
    PLANET_NAMES = {
        SUN: "Sun",
        MOON: "Moon", 
        MARS: "Mars",
        MERCURY: "Mercury",
        JUPITER: "Jupiter",
        VENUS: "Venus",
        SATURN: "Saturn",
        RAHU: "Rahu",
        KETU: "Ketu"
    }
    
    # Zodiac signs
    SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    # Nakshatras
    NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    # Nakshatra lords
    NAKSHATRA_LORDS = [
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
        "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
        "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
        "Jupiter", "Saturn", "Mercury"
    ]

    def __init__(self, birth_date: date, birth_time: time, latitude: float, longitude: float, timezone: str = "Asia/Kolkata"):
        """Initialize chart calculation."""
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        
        # Convert to Julian day number
        self.jd = swe.julday(
            birth_date.year, birth_date.month, birth_date.day,
            birth_time.hour + birth_time.minute/60.0 + birth_time.second/3600.0,
            swe.GREG_CAL
        )
        
        # Set ephemeris path
        swe.set_ephe_path()

    def calculate_planetary_positions(self) -> Dict[str, Dict]:
        """Calculate positions of all planets."""
        positions = {}
        
        planets = [self.SUN, self.MOON, self.MARS, self.MERCURY, self.JUPITER, self.VENUS, self.SATURN, self.RAHU]
        
        for planet in planets:
            try:
                # Calculate planet position
                planet_pos = swe.calc_ut(self.jd, planet, swe.FLG_SWIEPH)[0]
                longitude = planet_pos[0]
                
                # Convert to sign and degree
                sign_num = int(longitude / 30)
                degree_in_sign = longitude % 30
                
                # Calculate nakshatra
                nakshatra_num = int(longitude / 13.333)
                nakshatra_degree = longitude % 13.333
                
                positions[self.PLANET_NAMES[planet]] = {
                    "longitude": longitude,
                    "sign": self.SIGNS[sign_num],
                    "degree": round(degree_in_sign, 2),
                    "nakshatra": self.NAKSHATRAS[nakshatra_num],
                    "nakshatra_lord": self.NAKSHATRAS_LORDS[nakshatra_num],
                    "nakshatra_degree": round(nakshatra_degree, 2)
                }
                
            except Exception as e:
                logger.error(f"Error calculating position for {self.PLANET_NAMES[planet]}: {e}")
                positions[self.PLANET_NAMES[planet]] = {
                    "longitude": 0,
                    "sign": "Unknown",
                    "degree": 0,
                    "nakshatra": "Unknown",
                    "nakshatra_lord": "Unknown",
                    "nakshatra_degree": 0
                }
        
        # Calculate Ketu (180 degrees from Rahu)
        if "Rahu" in positions:
            rahu_long = positions["Rahu"]["longitude"]
            ketu_long = (rahu_long + 180) % 360
            
            sign_num = int(ketu_long / 30)
            degree_in_sign = ketu_long % 30
            nakshatra_num = int(ketu_long / 13.333)
            nakshatra_degree = ketu_long % 13.333
            
            positions["Ketu"] = {
                "longitude": ketu_long,
                "sign": self.SIGNS[sign_num],
                "degree": round(degree_in_sign, 2),
                "nakshatra": self.NAKSHATRAS[nakshatra_num],
                "nakshatra_lord": self.NAKSHATRAS_LORDS[nakshatra_num],
                "nakshatra_degree": round(nakshatra_degree, 2)
            }
        
        return positions

    def calculate_ascendant(self) -> Dict:
        """Calculate ascendant (rising sign)."""
        try:
            # Calculate ascendant
            asc_pos = swe.houses(self.jd, self.latitude, self.longitude, b'P')[0]
            asc_longitude = asc_pos[0]
            
            sign_num = int(asc_longitude / 30)
            degree_in_sign = asc_longitude % 30
            
            return {
                "longitude": asc_longitude,
                "sign": self.SIGNS[sign_num],
                "degree": round(degree_in_sign, 2)
            }
        except Exception as e:
            logger.error(f"Error calculating ascendant: {e}")
            return {
                "longitude": 0,
                "sign": "Unknown",
                "degree": 0
            }

    def calculate_houses(self) -> List[Dict]:
        """Calculate house cusps."""
        try:
            # Calculate house cusps
            houses = swe.houses(self.jd, self.latitude, self.longitude, b'P')[0]
            
            house_data = []
            for i, house_longitude in enumerate(houses):
                sign_num = int(house_longitude / 30)
                degree_in_sign = house_longitude % 30
                
                house_data.append({
                    "house": i + 1,
                    "longitude": house_longitude,
                    "sign": self.SIGNS[sign_num],
                    "degree": round(degree_in_sign, 2)
                })
            
            return house_data
        except Exception as e:
            logger.error(f"Error calculating houses: {e}")
            return []

    def calculate_divisional_chart(self, division: int) -> Dict:
        """Calculate divisional chart (Varga)."""
        # TODO: Implement divisional chart calculations
        # This is a complex calculation that requires special algorithms
        return {"message": f"Divisional chart {division} not implemented"}

    def get_chart_summary(self) -> Dict:
        """Get complete chart summary."""
        positions = self.calculate_planetary_positions()
        ascendant = self.calculate_ascendant()
        houses = self.calculate_houses()
        
        return {
            "birth_data": {
                "date": self.birth_date.isoformat(),
                "time": self.birth_time.isoformat(),
                "latitude": self.latitude,
                "longitude": self.longitude,
                "timezone": self.timezone
            },
            "ascendant": ascendant,
            "planetary_positions": positions,
            "houses": houses,
            "calculated_at": datetime.now().isoformat()
        }
