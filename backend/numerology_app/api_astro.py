# backend/numerology_app/api_astro.py
from __future__ import annotations
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from astral import LocationInfo
from astral.sun import sun
from datetime import date, timedelta
import pytz

router = APIRouter()

class Panchangam(BaseModel):
    date: str
    sunrise: str
    sunset: str
    rahu: dict
    yama: dict
    gulika: dict

# Fractions (weekday 0=Mon .. 6=Sun)
RAHU_FRAC = {0:(1,2), 1:(6,7), 2:(4,5), 3:(5,6), 4:(3,4), 5:(2,3), 6:(7,8)}
YAMA_FRAC = {0:(5,6), 1:(4,5), 2:(3,4), 3:(2,3), 4:(1,2), 5:(7,8), 6:(6,7)}
GULI_FRAC = {0:(3,4), 1:(2,3), 2:(1,2), 3:(7,8), 4:(6,7), 5:(5,6), 6:(4,5)}

def window_for(sunrise, sunset, slot_pair):
    day_len = (sunset - sunrise).total_seconds()
    slot_len = day_len / 8.0
    s_idx, e_idx = slot_pair
    start = sunrise + timedelta(seconds=(s_idx-1)*slot_len)
    end   = sunrise + timedelta(seconds=(e_idx-1)*slot_len)
    return start, end

@router.get("/astro/panchangam/today", response_model=Panchangam)
def panchangam_today(
    lat: float = Query(...),
    lon: float = Query(...),
    tz: str = Query("Asia/Kolkata")
):
    try:
        tzinfo = pytz.timezone(tz)
    except Exception:
        raise HTTPException(400, "Invalid timezone")

    loc = LocationInfo(latitude=lat, longitude=lon, timezone=tz)
    today = date.today()
    sdict = sun(loc.observer, date=today, tzinfo=tzinfo)
    sr, ss = sdict["sunrise"], sdict["sunset"]

    wd = today.weekday()
    rahu_s, rahu_e = window_for(sr, ss, RAHU_FRAC[wd])
    yama_s, yama_e = window_for(sr, ss, YAMA_FRAC[wd])
    guli_s, guli_e = window_for(sr, ss, GULI_FRAC[wd])

    fmt = "%H:%M"
    return Panchangam(
        date=str(today),
        sunrise=sr.strftime(fmt),
        sunset=ss.strftime(fmt),
        rahu={"start": rahu_s.strftime(fmt), "end": rahu_e.strftime(fmt)},
        yama={"start": yama_s.strftime(fmt), "end": yama_e.strftime(fmt)},
        gulika={"start": guli_s.strftime(fmt), "end": guli_e.strftime(fmt)},
    )
