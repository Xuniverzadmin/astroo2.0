# backend/numerology_app/api_calendar.py
from fastapi import APIRouter, Response, HTTPException, Query
from ics import Calendar, Event
from datetime import date, timedelta, datetime
import pytz
from .api_panchangam import RAHU_FRAC, YAMA_FRAC, GULIKA_FRAC, window_for
from astral import LocationInfo
from astral.sun import sun

router = APIRouter()

@router.get("/calendar.ics")
async def calendar_ics(lat: float = Query(...), lon: float = Query(...), tz: str = "Asia/Kolkata", days: int = 7):
    if days < 1 or days > 60:
        raise HTTPException(400, "days must be 1..60")

    tzinfo = pytz.timezone(tz)
    cal = Calendar()
    loc = LocationInfo(latitude=lat, longitude=lon, timezone=tz)

    for i in range(days):
        d = date.today() + timedelta(days=i)
        sdict = sun(loc.observer, date=d, tzinfo=tzinfo)
        sr, ss = sdict["sunrise"], sdict["sunset"]
        wd = d.weekday()
        for label, table in [("Rahu Kalam", RAHU_FRAC), ("Yamaganda", YAMA_FRAC), ("Gulikai", GULIKA_FRAC)]:
            s,e = window_for(sr, ss, table[wd])
            ev = Event(name=f"{label}", begin=s, end=e, description=f"{label} for {d.isoformat()}")
            cal.events.add(ev)

    ics_bytes = cal.serialize().encode("utf-8")
    return Response(content=ics_bytes, media_type="text/calendar")
# --- IGNORE ---