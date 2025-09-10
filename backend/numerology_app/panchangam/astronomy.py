"""
Astronomy module for Panchangam calculations using Skyfield.

This module provides astronomical calculations required for Vedic panchangam
computations including sun and moon positions, sunrise/sunset times, and
sidereal longitude calculations with Lahiri ayanamsa.
"""

import math
import os
from datetime import datetime, date, timezone
from typing import Tuple, Optional
import zoneinfo

from skyfield.api import load, wgs84, N, E
from skyfield import almanac
from skyfield.timelib import Time
from skyfield.positionlib import Apparent
from skyfield.constants import AU_KM

# Ephemeris configuration
EPH_PATH = os.getenv("EPHEMERIS_FILE", "/app/data/de421.bsp")
ts = load.timescale()

def get_ephemeris():
    """Load ephemeris from disk (no network download)"""
    return load(EPH_PATH)

def get_observer(lat: float, lon: float, elevation_m: float = 0.0):
    """
    Build a Skyfield geographic position using the modern API.
    lat, lon in decimal degrees; east/north positive.
    """
    return wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon, elevation_m=elevation_m)

def sunrise_sunset_local(date_yyyy_mm_dd: str, lat: float, lon: float, tz_name: str):
    """
    Returns (sunrise_local_iso, sunset_local_iso) strings.
    Handles the civil-twilight refraction by using almanac.sunrise_sunset().
    """
    eph = get_ephemeris()
    tz = zoneinfo.ZoneInfo(tz_name)

    # Build time window: local calendar day → UTC boundaries
    day_start_local = datetime.fromisoformat(f"{date_yyyy_mm_dd}T00:00:00").replace(tzinfo=tz)
    day_end_local   = day_start_local.replace(hour=23, minute=59, second=59)

    t0 = ts.from_datetime(day_start_local.astimezone(timezone.utc))
    t1 = ts.from_datetime(day_end_local.astimezone(timezone.utc))

    topos = get_observer(lat, lon)
    f = almanac.sunrise_sunset(eph, topos)
    times, events = almanac.find_discrete(t0, t1, f)

    sunrise_utc = None
    sunset_utc = None
    for t, ev in zip(times, events):
        if ev == 1 and sunrise_utc is None:
            sunrise_utc = t.utc_datetime().replace(tzinfo=timezone.utc)
        elif ev == 0 and sunset_utc is None:
            sunset_utc = t.utc_datetime().replace(tzinfo=timezone.utc)

    sunrise_local = sunrise_utc.astimezone(tz).isoformat() if sunrise_utc else None
    sunset_local  = sunset_utc.astimezone(tz).isoformat() if sunset_utc else None
    return sunrise_local, sunset_local

def sun_moon_ecliptic_longitudes(dt: datetime, lat: float, lon: float):
    """Get sun and moon ecliptic longitudes for tithi/nakshatra calculations"""
    eph = get_ephemeris()
    t = ts.from_datetime(dt.astimezone(timezone.utc))
    # Use geocentric longitudes (observer not needed here)
    e = eph['earth']
    sun = e.at(t).observe(eph['sun']).apparent().ecliptic_latlon()[1].degrees % 360.0
    moon = e.at(t).observe(eph['moon']).apparent().ecliptic_latlon()[1].degrees % 360.0
    return sun, moon


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
        """
        # Use the new modern helper function
        sunrise_iso, sunset_iso = sunrise_sunset_local(date_obj.isoformat(), lat, lon, tz)
        
        if sunrise_iso and sunset_iso:
            # Convert ISO strings back to datetime objects
            sunrise_dt = datetime.fromisoformat(sunrise_iso.replace('Z', '+00:00'))
            sunset_dt = datetime.fromisoformat(sunset_iso.replace('Z', '+00:00'))
            return sunrise_dt, sunset_dt
        else:
            # Fallback to approximate times if calculation fails
            tz_obj = zoneinfo.ZoneInfo(tz)
            base_date = datetime.combine(date_obj, datetime.min.time()).replace(tzinfo=tz_obj)
            return base_date.replace(hour=6), base_date.replace(hour=18)
    
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
