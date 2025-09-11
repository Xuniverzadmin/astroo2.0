# backend/numerology_app/vedic_dasha.py
"""
Vedic Dasha calculations using Swiss Ephemeris.
Provides Vimshottari Dasha, Antardasha, and other planetary periods.
"""

import swisseph as swe
import math
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Tuple, Optional
import pytz
import logging

logger = logging.getLogger(__name__)

class VedicDasha:
    """Main class for Vedic Dasha calculations."""
    
    # Vimshottari Dasha periods (in years)
    VIMSHOTTARI_PERIODS = {
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
        "Ketu": 7,
        "Venus": 20
    }
    
    # Dasha sequence
    DASHA_SEQUENCE = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
    
    # Planet constants for Swiss Ephemeris
    PLANET_CONSTANTS = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": swe.MEAN_NODE
    }

    def __init__(self, birth_date: date, birth_time: time, latitude: float, longitude: float, timezone: str = "Asia/Kolkata"):
        """Initialize dasha calculation."""
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

    def calculate_moon_nakshatra(self) -> Tuple[int, float]:
        """Calculate moon's nakshatra at birth."""
        try:
            # Get moon position
            moon_pos = swe.calc_ut(self.jd, swe.MOON, swe.FLG_SWIEPH)[0]
            moon_longitude = moon_pos[0]
            
            # Calculate nakshatra (27 nakshatras, each 13.333 degrees)
            nakshatra_num = int(moon_longitude / 13.333) + 1
            nakshatra_degree = moon_longitude % 13.333
            
            return nakshatra_num, nakshatra_degree
        except Exception as e:
            logger.error(f"Error calculating moon nakshatra: {e}")
            return 1, 0.0

    def calculate_dasha_lord(self) -> str:
        """Calculate the dasha lord based on moon's nakshatra."""
        nakshatra_num, nakshatra_degree = self.calculate_moon_nakshatra()
        
        # Each nakshatra is ruled by a specific planet
        nakshatra_lords = [
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
            "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
            "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
            "Jupiter", "Saturn", "Mercury"
        ]
        
        return nakshatra_lords[nakshatra_num - 1]

    def calculate_dasha_start_date(self, dasha_lord: str) -> date:
        """Calculate the start date of the current dasha."""
        nakshatra_num, nakshatra_degree = self.calculate_moon_nakshatra()
        
        # Calculate remaining period of current dasha
        total_nakshatra_degrees = 13.333
        remaining_degrees = total_nakshatra_degrees - nakshatra_degree
        
        # Calculate remaining time in current dasha
        dasha_period_years = self.VIMSHOTTARI_PERIODS[dasha_lord]
        remaining_time_years = (remaining_degrees / total_nakshatra_degrees) * dasha_period_years
        
        # Calculate start date
        start_date = self.birth_date + timedelta(days=remaining_time_years * 365.25)
        
        return start_date

    def calculate_dasha_timeline(self, years_ahead: int = 120) -> List[Dict]:
        """Calculate complete dasha timeline."""
        try:
            # Get current dasha lord
            current_dasha_lord = self.calculate_dasha_lord()
            current_dasha_start = self.calculate_dasha_start_date(current_dasha_lord)
            
            timeline = []
            current_date = current_dasha_start
            
            # Find current dasha lord in sequence
            current_index = self.DASHA_SEQUENCE.index(current_dasha_lord)
            
            # Calculate dasha periods
            for i in range(9):  # 9 planets in sequence
                planet_index = (current_index + i) % 9
                planet = self.DASHA_SEQUENCE[planet_index]
                period_years = self.VIMSHOTTARI_PERIODS[planet]
                
                start_date = current_date
                end_date = current_date + timedelta(days=period_years * 365.25)
                
                timeline.append({
                    "planet": planet,
                    "start_date": start_date,
                    "end_date": end_date,
                    "duration_years": period_years,
                    "is_active": i == 0
                })
                
                current_date = end_date
                
                # Stop if we've covered enough years
                if (end_date - self.birth_date).days > years_ahead * 365:
                    break
            
            return timeline
            
        except Exception as e:
            logger.error(f"Error calculating dasha timeline: {e}")
            return []

    def calculate_antardasha_sequence(self, dasha_lord: str, start_date: date, end_date: date) -> List[Dict]:
        """Calculate antardasha sequence for a given dasha period."""
        try:
            # Antardasha follows the same sequence as dasha
            dasha_index = self.DASHA_SEQUENCE.index(dasha_lord)
            dasha_period_days = (end_date - start_date).days
            
            antardasha_sequence = []
            current_date = start_date
            
            for i in range(9):  # 9 planets in sequence
                planet_index = (dasha_index + i) % 9
                planet = self.DASHA_SEQUENCE[planet_index]
                period_years = self.VIMSHOTTARI_PERIODS[planet]
                
                # Calculate antardasha period
                antardasha_days = int((period_years / 120) * dasha_period_days)
                antardasha_end = current_date + timedelta(days=antardasha_days)
                
                antardasha_sequence.append({
                    "planet": planet,
                    "start_date": current_date,
                    "end_date": antardasha_end,
                    "duration_days": antardasha_days,
                    "is_active": i == 0
                })
                
                current_date = antardasha_end
            
            return antardasha_sequence
            
        except Exception as e:
            logger.error(f"Error calculating antardasha sequence: {e}")
            return []

    def get_current_dasha(self) -> Dict:
        """Get current active dasha and antardasha."""
        try:
            timeline = self.calculate_dasha_timeline()
            if not timeline:
                return {"error": "Could not calculate dasha timeline"}
            
            current_dasha = timeline[0]  # First one is current
            
            # Calculate current antardasha
            antardasha_sequence = self.calculate_antardasha_sequence(
                current_dasha["planet"],
                current_dasha["start_date"],
                current_dasha["end_date"]
            )
            
            current_antardasha = antardasha_sequence[0] if antardasha_sequence else None
            
            return {
                "current_dasha": current_dasha,
                "current_antardasha": current_antardasha,
                "calculated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting current dasha: {e}")
            return {"error": f"Could not calculate current dasha: {e}"}

    def get_dasha_summary(self) -> Dict:
        """Get complete dasha summary."""
        timeline = self.calculate_dasha_timeline()
        current_info = self.get_current_dasha()
        
        return {
            "birth_data": {
                "date": self.birth_date.isoformat(),
                "time": self.birth_time.isoformat(),
                "latitude": self.latitude,
                "longitude": self.longitude,
                "timezone": self.timezone
            },
            "dasha_timeline": timeline,
            "current_dasha": current_info.get("current_dasha"),
            "current_antardasha": current_info.get("current_antardasha"),
            "calculated_at": datetime.now().isoformat()
        }
