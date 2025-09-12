from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, Tuple
from astral.sun import sun
from astral import Observer
from zoneinfo import ZoneInfo

# Day-of-week: Monday=0 ... Sunday=6 (Python's datetime.weekday())
# Rahu, Yamaganda, Gulikai segment indices (1..8) from sunrise (inclusive)
_RAHU_SEG = {6: 8, 0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3}       # Sun,Mon,...Sat
_YAMA_SEG = {6: 5, 0: 4, 1: 3, 2: 2, 3: 1, 4: 7, 5: 6}
_GULI_SEG = {6: 6, 0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 7}

@dataclass
class Windows:
    sunrise: datetime
    sunset: datetime
    parts: Tuple[Tuple[datetime, datetime], ...]
    rahu: Tuple[datetime, datetime]
    yamaganda: Tuple[datetime, datetime]
    gulikai: Tuple[datetime, datetime]
    best_windows: Tuple[Tuple[datetime, datetime], ...]  # daylight minus the three inauspicious parts

def _segments(sunrise: datetime, sunset: datetime):
    """Split daylight into 8 equal segments."""
    span = (sunset - sunrise)
    step = span / 8
    parts = tuple((sunrise + i * step, sunrise + (i + 1) * step) for i in range(8))
    return parts

def _fmt(dt: datetime) -> str:
    return dt.strftime("%H:%M")

def format_window(w: Tuple[datetime, datetime]) -> str:
    return f"{_fmt(w[0])}-{_fmt(w[1])}"

def compute_windows(
    for_date: date,
    lat: float,
    lon: float,
    tz: str = "Asia/Kolkata",
) -> Windows:
    tzinfo = ZoneInfo(tz)
    obs = Observer(latitude=lat, longitude=lon)
    s = sun(observer=obs, date=for_date, tzinfo=tzinfo)
    sunrise = s["sunrise"]
    sunset  = s["sunset"]
    parts = _segments(sunrise, sunset)

    # weekday map (Python Mon=0 ... Sun=6). Our dicts use Sun=6.
    wd = for_date.weekday()

    rahu_idx = _RAHU_SEG[wd] - 1
    yama_idx = _YAMA_SEG[wd] - 1
    guli_idx = _GULI_SEG[wd] - 1

    rahu = parts[rahu_idx]
    yama = parts[yama_idx]
    guli = parts[guli_idx]

    # Best windows = all segments except the three above
    bad = {rahu_idx, yama_idx, guli_idx}
    best = tuple(p for i, p in enumerate(parts) if i not in bad)

    return Windows(
        sunrise=sunrise, sunset=sunset, parts=parts,
        rahu=rahu, yamaganda=yama, gulikai=guli,
        best_windows=best
    )
