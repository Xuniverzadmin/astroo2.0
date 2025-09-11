# backend/numerology_app/api_panchangam.py
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
from astral import LocationInfo
from astral.sun import sun
from datetime import date, timedelta
import pytz
from .panchangam.core import assemble_panchangam

router = APIRouter()

class Panchangam(BaseModel):
    date: str
    sunrise: str
    sunset: str
    rahu: dict
    yama: dict
    gulika: dict

# Fractions (weekday 0=Monday → 6=Sunday)
RAHU_FRAC = {
    0: (1,2), 1: (6,7), 2: (4,5), 3: (5,6), 4: (3,4), 5: (2,3), 6: (7,8)
}
YAMA_FRAC = {
    0: (5,6), 1: (4,5), 2: (3,4), 3: (2,3), 4: (1,2), 5: (7,8), 6: (6,7)
}
GULIKA_FRAC = {
    0: (3,4), 1: (2,3), 2: (1,2), 3: (7,8), 4: (6,7), 5: (5,6), 6: (4,5)
}

def window_for(sunrise, sunset, slot_pair):
    day_len = (sunset - sunrise).total_seconds()
    slot_len = day_len / 8.0
    s_idx, e_idx = slot_pair
    start = sunrise + timedelta(seconds=(s_idx-1)*slot_len)
    end   = sunrise + timedelta(seconds=(e_idx-1)*slot_len)
    return start, end

@router.get("/panchangam/today", response_model=Panchangam)
async def panchangam_today(
    lat: float = Query(...), lon: float = Query(...),
    tz: str = Query("Asia/Kolkata")
):
    """Get panchangam for today - convenience endpoint."""
    tzinfo = pytz.timezone(tz)
    loc = LocationInfo(latitude=lat, longitude=lon, timezone=tz)
    today = date.today()
    sdict = sun(loc.observer, date=today, tzinfo=tzinfo)
    sr, ss = sdict["sunrise"], sdict["sunset"]

    wd = today.weekday()  # Monday=0..Sunday=6
    rahu_s, rahu_e     = window_for(sr, ss, RAHU_FRAC[wd])
    yama_s, yama_e     = window_for(sr, ss, YAMA_FRAC[wd])
    gulika_s, gulika_e = window_for(sr, ss, GULIKA_FRAC[wd])

    fmt = "%H:%M"
    return Panchangam(
        date=str(today),
        sunrise=sr.strftime(fmt),
        sunset=ss.strftime(fmt),
        rahu={"start": rahu_s.strftime(fmt), "end": rahu_e.strftime(fmt)},
        yama={"start": yama_s.strftime(fmt), "end": yama_e.strftime(fmt)},
        gulika={"start": gulika_s.strftime(fmt), "end": gulika_e.strftime(fmt)},
    )

@router.get("/diag/panchangam/{the_date}", response_class=PlainTextResponse)
def diag_panchangam(
    the_date: date,
    lat: float = Query(13.0827),
    lon: float = Query(80.2707),
    tz: str = Query("Asia/Kolkata"),
):
    try:
        data = assemble_panchangam(the_date, lat, lon, tz, settings=None)
        lines = [
            f"Date: {the_date}  TZ: {tz}  LatLon: {lat},{lon}",
            f"Sunrise: {data.get('sunrise')}  Sunset: {data.get('sunset')}",
            f"Tithi: {data.get('tithi',{}).get('name')} ({data.get('tithi',{}).get('percentage', 'N/A')}%)",
            f"Nakshatra: {data.get('nakshatra',{}).get('name')} ({data.get('nakshatra',{}).get('percentage', 'N/A')}%)",
            f"Yoga: {data.get('yoga',{}).get('name')}  Karana: {data.get('karana',{}).get('name')}",
            f"Rahu Kalam: {data.get('rahu_kalam')}",
            f"Yama Gandam: {data.get('yama_gandam')}",
            f"Gulikai Kalam: {data.get('gulikai_kalam')}",
            f"Gowri Panchangam: {data.get('gowri_panchangam', {}).get('periods', {})}",
        ]
        return "\n".join(lines)
    except Exception:
        import traceback
        return "ERROR\n" + traceback.format_exc()


@router.get("/api/panchangam/{the_date}", response_class=JSONResponse)
async def panchangam_by_date(
    the_date: date = Path(..., description="Date for panchangam calculation (YYYY-MM-DD)"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query("Asia/Kolkata", description="Timezone string"),
):
    """
    Returns Panchangam for any date in standard JSON for frontend use.
    This is the stable, production-grade route that always returns valid JSON.
    """
    try:
        # Try your real calculation
        result = assemble_panchangam(the_date, lat, lon, tz, settings=None)
        if not result:
            raise HTTPException(status_code=404, detail="Panchangam not found")
        return result
    except Exception as e:
        # Always return a JSON error, never crash the app
        import traceback
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Error generating panchangam for {the_date}: {str(e)}",
                "trace": traceback.format_exc()
            }
        )
