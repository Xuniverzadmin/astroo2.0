"""
Astronomy module for Panchangam calculations using Skyfield.

This module provides astronomical calculations required for Vedic panchangam
computations including sun and moon positions, sunrise/sunset times, and
sidereal longitude calculations with Lahiri ayanamsa.
"""

import math
from datetime import datetime, date
from typing import Tuple, Optional
import pytz

from skyfield.api import load, Topos
from skyfield.timelib import Time
from skyfield.positionlib import Apparent
from skyfield.constants import AU_KM


class AstronomyEngine:
    """
    Astronomy engine for panchangam calculations using Skyfield.
    
    Uses DE440s ephemeris for accuracy and caches timescale for performance.
    """
    
    def __init__(self):
        """Initialize the astronomy engine with Skyfield data."""
        # Load DE440s ephemeris (smaller than DE441 but still accurate)
        self.eph = load('de440s.bsp')
        self.timescale = load.timescale()
        
        # Cache for timescale to avoid reloading
        self._ts_cache = {}
    
    def get_timescale(self) -> Time:
        """Get cached timescale for performance."""
        return self.timescale
    
    def sun_longitude_ecliptic(self, dt: datetime) -> float:
        """
        Calculate sun's longitude in ecliptic coordinates (sidereal with Lahiri ayanamsa).
        
        Args:
            dt: Date and time for calculation
            
        Returns:
            Sun's longitude in degrees (0-360)
            
        Formula:
            - Get apparent position of sun from Skyfield
            - Convert to ecliptic coordinates
            - Apply Lahiri ayanamsa correction (50.2388475° for 2000.0 epoch)
        """
        ts = self.get_timescale()
        t = ts.from_datetime(dt)
        
        # Get sun position
        sun = self.eph['sun']
        earth = self.eph['earth']
        
        # Calculate apparent position
        astrometric = earth.at(t).observe(sun)
        apparent = astrometric.apparent()
        
        # Get ecliptic coordinates
        lat, lon, distance = apparent.ecliptic_latlon()
        
        # Convert to degrees and apply Lahiri ayanamsa
        sun_longitude = lon.degrees
        lahiri_ayanamsa = 50.2388475  # Degrees for 2000.0 epoch
        
        # Apply ayanamsa correction for sidereal longitude
        sidereal_longitude = (sun_longitude - lahiri_ayanamsa) % 360
        
        return sidereal_longitude
    
    def moon_longitude_ecliptic(self, dt: datetime) -> float:
        """
        Calculate moon's longitude in ecliptic coordinates (sidereal with Lahiri ayanamsa).
        
        Args:
            dt: Date and time for calculation
            
        Returns:
            Moon's longitude in degrees (0-360)
            
        Formula:
            - Get apparent position of moon from Skyfield
            - Convert to ecliptic coordinates
            - Apply Lahiri ayanamsa correction
        """
        ts = self.get_timescale()
        t = ts.from_datetime(dt)
        
        # Get moon position
        moon = self.eph['moon']
        earth = self.eph['earth']
        
        # Calculate apparent position
        astrometric = earth.at(t).observe(moon)
        apparent = astrometric.apparent()
        
        # Get ecliptic coordinates
        lat, lon, distance = apparent.ecliptic_latlon()
        
        # Convert to degrees and apply Lahiri ayanamsa
        moon_longitude = lon.degrees
        lahiri_ayanamsa = 50.2388475  # Degrees for 2000.0 epoch
        
        # Apply ayanamsa correction for sidereal longitude
        sidereal_longitude = (moon_longitude - lahiri_ayanamsa) % 360
        
        return sidereal_longitude
    
    def sunrise_sunset(self, date_obj: date, lat: float, lon: float, tz: str) -> Tuple[datetime, datetime]:
        """
        Calculate sunrise and sunset times for a given date and location.
        
        Args:
            date_obj: Date for calculation
            lat: Latitude in degrees
            lon: Longitude in degrees  
            tz: Timezone string (e.g., 'Asia/Kolkata')
            
        Returns:
            Tuple of (sunrise_time, sunset_time) as datetime objects
            
        Formula:
            - Solve for altitude = -0.833° (standard sunrise/sunset altitude)
            - Account for atmospheric refraction
            - Convert to local timezone
        """
        ts = self.get_timescale()
        timezone = pytz.timezone(tz)
        
        # Create location with proper units
        location = Topos(latitude_degrees=lat, longitude_degrees=lon)
        
        # Get sun
        sun = self.eph['sun']
        earth = self.eph['earth']
        
        # Start with approximate times (6 AM and 6 PM local time)
        base_date = datetime.combine(date_obj, datetime.min.time())
        local_base = timezone.localize(base_date)
        
        # Convert to UTC for Skyfield
        utc_base = local_base.astimezone(pytz.UTC)
        
        # Calculate sunrise (altitude = -0.833°)
        sunrise_utc = self._find_sun_event(
            utc_base, location, sun, earth, ts, 
            target_altitude=-0.833, is_sunrise=True
        )
        
        # Calculate sunset (altitude = -0.833°)
        sunset_utc = self._find_sun_event(
            utc_base, location, sun, earth, ts,
            target_altitude=-0.833, is_sunrise=False
        )
        
        # Convert back to local time
        sunrise_local = sunrise_utc.astimezone(timezone)
        sunset_local = sunset_utc.astimezone(timezone)
        
        return sunrise_local, sunset_local
    
    def _find_sun_event(self, base_time: datetime, location: Topos, 
                       sun, earth, ts: Time, target_altitude: float, 
                       is_sunrise: bool) -> datetime:
        """
        Find sun event (sunrise/sunset) using iterative altitude solving.
        
        Args:
            base_time: Base time for search
            location: Geographic location
            sun: Sun object from ephemeris
            earth: Earth object from ephemeris
            ts: Timescale
            target_altitude: Target altitude in degrees (-0.833 for sunrise/sunset)
            is_sunrise: True for sunrise, False for sunset
            
        Returns:
            UTC datetime of the event
        """
        # Start with approximate time
        if is_sunrise:
            search_time = base_time.replace(hour=6, minute=0, second=0)
        else:
            search_time = base_time.replace(hour=18, minute=0, second=0)
        
        # Iterative search for exact time
        for iteration in range(10):  # Max 10 iterations
            t = ts.from_datetime(search_time)
            
            # Calculate sun position
            astrometric = earth.at(t).observe(sun)
            apparent = astrometric.apparent()
            
            # Calculate altitude at location
            alt, az, distance = apparent.altaz(location)
            current_altitude = alt.degrees
            
            # Check if we're close enough
            if abs(current_altitude - target_altitude) < 0.01:
                break
            
            # Adjust time based on altitude difference
            time_adjustment = (current_altitude - target_altitude) * 4  # Rough conversion
            search_time = search_time.replace(
                hour=search_time.hour,
                minute=max(0, min(59, search_time.minute + int(time_adjustment))),
                second=0
            )
        
        return search_time


# Global instance for use across the application
astronomy_engine = AstronomyEngine()


def get_sun_longitude(dt: datetime) -> float:
    """Convenience function to get sun's sidereal longitude."""
    return astronomy_engine.sun_longitude_ecliptic(dt)


def get_moon_longitude(dt: datetime) -> float:
    """Convenience function to get moon's sidereal longitude."""
    return astronomy_engine.moon_longitude_ecliptic(dt)


def get_sunrise_sunset(date_obj: date, lat: float, lon: float, tz: str) -> Tuple[datetime, datetime]:
    """Convenience function to get sunrise and sunset times."""
    return astronomy_engine.sunrise_sunset(date_obj, lat, lon, tz)


# TODO: Add unit tests for:
# - sun_longitude_ecliptic() with known dates
# - moon_longitude_ecliptic() with known dates  
# - sunrise_sunset() with known locations and dates
# - Edge cases: polar regions, date line crossing
# - Accuracy validation against published ephemeris data
