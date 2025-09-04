from __future__ import annotations
from datetime import datetime, timedelta

def _segment_window(sr: datetime, ss: datetime, segment_number_1based: int) -> tuple[datetime, datetime]:
    """
    Given sunrise (sr) and sunset (ss), divide daylight into 8 equal parts
    and return the start/end datetimes for the requested 1-based segment number (1..8).
    """
    if not (1 <= segment_number_1based <= 8):
        raise ValueError("segment_number_1based must be in 1..8")
    daylight = ss - sr
    part = daylight / 8
    start = sr + part * (segment_number_1based - 1)
    end = start + part
    return start, end

def day_segments(sr: datetime, ss: datetime, weekday: int) -> tuple[str, str, str]:
    """
    Compute Rahu Kaal, Yamagandam, and Gulika windows for a given weekday.
    `weekday` is Python's date.weekday(): Monday=0 .. Sunday=6.
    Returns strings like 'HH:MM-HH:MM'.
    """
    # Standard mapping of segment positions (1..8)
    # Sources describe: divide sunrise->sunset into 8 equal parts. Rahu/Yama/Gulika
    # occupy fixed segment numbers per weekday. (See product docs/citations in app.)
    rahu_map      = [2, 7, 5, 6, 4, 3, 8]  # Mon..Sun
    yama_map      = [4, 3, 2, 1, 7, 6, 5]  # Mon..Sun
    gulika_map    = [6, 5, 4, 3, 2, 1, 7]  # Mon..Sun

    r_start, r_end = _segment_window(sr, ss, rahu_map[weekday])
    y_start, y_end = _segment_window(sr, ss, yama_map[weekday])
    g_start, g_end = _segment_window(sr, ss, gulika_map[weekday])

    def f(a: datetime, b: datetime) -> str:
        return f"{a.strftime('%H:%M')}-{b.strftime('%H:%M')}"

    return f(r_start, r_end), f(y_start, y_end), f(g_start, g_end)

def vedic_elements(d, lat, lon, tz) -> tuple[str, str, str, str]:
    """
    Placeholder for Tithi/Nakshatra/Yoga/Karana (requires lunar ephemerides).
    """
    return ("Tithi TBD", "Nakshatra TBD", "Yoga TBD", "Karana TBD")
