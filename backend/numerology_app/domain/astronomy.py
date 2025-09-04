from __future__ import annotations
from datetime import date, datetime
from zoneinfo import ZoneInfo

# Astral imports (supporting both v2/v3 styles)
try:
    from astral import Observer  # Astral >= 2
except ImportError:  # pragma: no cover
    Observer = None  # type: ignore

from astral.sun import sun

def solar_events(d: date, lat: float, lon: float, tz: str) -> tuple[datetime, datetime]:
    """
    Compute local sunrise and sunset (timezone-aware) using Astral.
    Returns (sunrise_dt, sunset_dt) as aware datetimes.
    """
    tzinfo = ZoneInfo(tz)

    if Observer is not None:
        obs = Observer(latitude=lat, longitude=lon)
        s = sun(observer=obs, date=d, tzinfo=tzinfo)
    else:
        # Fallback if Observer import path changes (rare)
        from astral import LocationInfo  # type: ignore
        loc = LocationInfo("", "", tz, lat, lon)
        s = sun(observer=loc.observer, date=d, tzinfo=tzinfo)

    sr = s["sunrise"].astimezone(tzinfo)
    ss = s["sunset"].astimezone(tzinfo)
    return sr, ss

def fmt_hhmm(dt: datetime) -> str:
    return dt.strftime("%H:%M")
