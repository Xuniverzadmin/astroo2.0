from typing import Optional
from timezonefinder import TimezoneFinder

def tz_from_latlon(lat: float, lon: float, default: str = "Asia/Kolkata") -> str:
    """
    Return IANA timezone string for given lat/lon.
    Falls back to `default` if not found or any error.
    """
    try:
        tf = TimezoneFinder()
        tz = tf.timezone_at(lat=lat, lng=lon)
        return tz or default
    except Exception:
        return default
