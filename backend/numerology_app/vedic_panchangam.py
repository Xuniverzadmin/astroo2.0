"""
Vedic Panchangam calculations using pyswisseph (Swiss Ephemeris).
Based on proven formulas for accurate Tithi, Nakshatra, Yoga, and Karana calculations.
"""

import swisseph as swe
import math
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional
import pytz


class Tithi:
    """Represents a Tithi (lunar day) with its properties."""
    def __init__(self, index: int, name_english: str, elapsed_percentage: float, end_time: Optional[datetime] = None):
        self.index = index
        self.name_english = name_english
        self.elapsed_percentage = elapsed_percentage
        self.end_time = end_time


class Nakshatra:
    """Represents a Nakshatra (lunar mansion) with its properties."""
    def __init__(self, index: int, name_english: str, elapsed_percentage: float, end_time: Optional[datetime] = None):
        self.index = index
        self.name_english = name_english
        self.elapsed_percentage = elapsed_percentage
        self.end_time = end_time


class Yoga:
    """Represents a Yoga with its properties."""
    def __init__(self, index: int, name_english: str, elapsed_percentage: float, end_time: Optional[datetime] = None):
        self.index = index
        self.name_english = name_english
        self.elapsed_percentage = elapsed_percentage
        self.end_time = end_time


class Karana:
    """Represents a Karana with its properties."""
    def __init__(self, name_english: str, elapsed_percentage: float, end_time: Optional[datetime] = None):
        self.name_english = name_english
        self.elapsed_percentage = elapsed_percentage
        self.end_time = end_time


class City:
    """Represents a city with its geographical and timezone information."""
    def __init__(self, name: str, latitude: float, longitude: float, timezone: str):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone


class Panchangam:
    """Main Panchangam calculator using Swiss Ephemeris."""
    
    # Tithi names
    TITHI_NAMES = [
        "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Purnima",
        "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Amavasya"
    ]
    
    # Nakshatra names
    NAKSHATRA_NAMES = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha",
        "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
        "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
        "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    
    # Yoga names
    YOGA_NAMES = [
        "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
        "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
        "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
        "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
        "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
        "Indra", "Vaidhriti"
    ]
    
    # Karana names
    KARANA_NAMES = [
        "Bava", "Balava", "Kaulava", "Taitila", "Gara",
        "Vanija", "Visti", "Shakuni", "Chatushpada", "Naga",
        "Kimstughna"
    ]

    def __init__(self, city: City, date_obj: date):
        self.city = city
        self.date_obj = date_obj
        self.tithi = None
        self.nakshatra = None
        self.yoga = None
        self.karana = None
        self.sunrise = None
        self.sunset = None

    def compute(self):
        """Compute all panchangam elements for the given date and location."""
        # Set ephemeris path (use default)
        swe.set_ephe_path()
        
        # Convert date to Julian day number
        jd = swe.julday(self.date_obj.year, self.date_obj.month, self.date_obj.day, swe.GREG_CAL)
        
        # Calculate sunrise and sunset
        self._calculate_sunrise_sunset(jd)
        
        # Calculate sun and moon positions
        sun_long = self._get_sun_longitude(jd)
        moon_long = self._get_moon_longitude(jd)
        
        # Calculate panchangam elements
        self._calculate_tithi(sun_long, moon_long, jd)
        self._calculate_nakshatra(moon_long, jd)
        self._calculate_yoga(sun_long, moon_long, jd)
        self._calculate_karana(jd)

    def _calculate_sunrise_sunset(self, jd: float):
        """Calculate sunrise and sunset times."""
        # Get timezone offset
        tz = pytz.timezone(self.city.timezone)
        utc_offset = tz.utcoffset(datetime.now()).total_seconds() / 3600
        
        # Calculate sunrise and sunset
        sunrise_jd = swe.rise_trans(jd, swe.SUN, "", swe.CALC_RISE, 
                                   swe.FLG_SWIEPH, self.city.longitude, self.city.latitude, 0, 0, 0)[1][0]
        sunset_jd = swe.rise_trans(jd, swe.SUN, "", swe.CALC_SET, 
                                  swe.FLG_SWIEPH, self.city.longitude, self.city.latitude, 0, 0, 0)[1][0]
        
        # Convert to datetime
        if sunrise_jd > 0:
            self.sunrise = swe.revjul(sunrise_jd, swe.GREG_CAL)
            self.sunrise = datetime(*[int(x) for x in self.sunrise[:6]])
        else:
            self.sunrise = datetime(self.date_obj.year, self.date_obj.month, self.date_obj.day, 6, 0)
            
        if sunset_jd > 0:
            self.sunset = swe.revjul(sunset_jd, swe.GREG_CAL)
            self.sunset = datetime(*[int(x) for x in self.sunset[:6]])
        else:
            self.sunset = datetime(self.date_obj.year, self.date_obj.month, self.date_obj.day, 18, 0)

    def _get_sun_longitude(self, jd: float) -> float:
        """Get sun's longitude."""
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)[0]
        return sun_pos[0]  # Longitude in degrees

    def _get_moon_longitude(self, jd: float) -> float:
        """Get moon's longitude."""
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH)[0]
        return moon_pos[0]  # Longitude in degrees

    def _calculate_tithi(self, sun_long: float, moon_long: float, jd: float):
        """Calculate Tithi (lunar day)."""
        # Tithi is the angular distance between sun and moon divided by 12 degrees
        tithi_diff = (moon_long - sun_long) % 360
        tithi_num = int(tithi_diff / 12) + 1
        
        # Calculate progress within the tithi
        tithi_progress = (tithi_diff % 12) / 12.0
        
        # Determine if it's Shukla or Krishna paksha
        if tithi_num <= 15:
            tithi_name = f"Shukla {self.TITHI_NAMES[tithi_num - 1]}"
        else:
            tithi_name = f"Krishna {self.TITHI_NAMES[tithi_num - 16]}"
        
        self.tithi = Tithi(tithi_num, tithi_name, tithi_progress)

    def _calculate_nakshatra(self, moon_long: float, jd: float):
        """Calculate Nakshatra (lunar mansion)."""
        # Nakshatra is moon's longitude divided by 13.333 degrees (360/27)
        nakshatra_diff = (moon_long - 0) % 360  # Start from Ashwini
        nakshatra_num = int(nakshatra_diff / 13.333) + 1
        
        # Calculate progress within the nakshatra
        nakshatra_progress = (nakshatra_diff % 13.333) / 13.333
        
        nakshatra_name = self.NAKSHATRA_NAMES[nakshatra_num - 1]
        self.nakshatra = Nakshatra(nakshatra_num, nakshatra_name, nakshatra_progress)

    def _calculate_yoga(self, sun_long: float, moon_long: float, jd: float):
        """Calculate Yoga."""
        # Yoga is the sum of sun and moon longitudes divided by 13.333 degrees
        yoga_sum = (sun_long + moon_long) % 360
        yoga_num = int(yoga_sum / 13.333) + 1
        
        # Calculate progress within the yoga
        yoga_progress = (yoga_sum % 13.333) / 13.333
        
        yoga_name = self.YOGA_NAMES[yoga_num - 1]
        self.yoga = Yoga(yoga_num, yoga_name, yoga_progress)

    def _calculate_karana(self, jd: float):
        """Calculate Karana."""
        # Karana is based on tithi
        if self.tithi:
            tithi_num = self.tithi.index
            tithi_progress = self.tithi.elapsed_percentage
            
            # Karana calculation based on tithi
            if tithi_progress < 0.5:
                karana_index = (tithi_num - 1) * 2
            else:
                karana_index = (tithi_num - 1) * 2 + 1
            
            karana_index = karana_index % 11
            karana_name = self.KARANA_NAMES[karana_index]
            
            # Calculate karana progress
            karana_progress = (tithi_progress * 2) % 1.0
            
            self.karana = Karana(karana_name, karana_progress)
