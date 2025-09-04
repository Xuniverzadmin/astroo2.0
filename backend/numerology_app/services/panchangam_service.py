from ..schemas.panchangam import PanchangamQuery, PanchangamOut
from ..adapters.timezone import tz_from_latlon
from ..domain.astronomy import solar_events, fmt_hhmm
from ..domain.vedic import day_segments, vedic_elements

def _cache_key(q: PanchangamQuery, tz: str) -> str:
    return f"panchangam:{q.date}:{q.lat:.4f}:{q.lon:.4f}:{tz}"

async def get_panchangam(q: PanchangamQuery, cache, settings) -> PanchangamOut:
    tz = q.tz or tz_from_latlon(q.lat, q.lon, default=settings.DEFAULT_TZ)

    key = _cache_key(q, tz)
    cached = await cache.get(key)
    if cached:
        return PanchangamOut(**cached)

    sr_dt, ss_dt = solar_events(q.date, q.lat, q.lon, tz)
    rahu, yama, gulika = day_segments(sr_dt, ss_dt, q.date.weekday())
    tithi, nak, yoga, karana = vedic_elements(q.date, q.lat, q.lon, tz)

    payload = PanchangamOut(
        sunrise=fmt_hhmm(sr_dt),
        sunset=fmt_hhmm(ss_dt),
        rahukaalam=rahu,
        yamagandam=yama,
        gulikai=gulika,
        tithi=tithi,
        nakshatra=nak,
        yoga=yoga,
        karana=karana,
    ).model_dump()

    await cache.set(key, payload, ttl=24*3600)
    return PanchangamOut(**payload)
