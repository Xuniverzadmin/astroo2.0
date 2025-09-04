from fastapi import APIRouter, Depends, HTTPException, Query
from ..schemas.astro import NumerologyIn, NumerologyOut, PanchangamOut, DailyHoroscopeIn, TarotIn, TarotOut
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/astro", tags=["astro"])

@router.post("/numerology", response_model=NumerologyOut)
def numerology(body: NumerologyIn, db=Depends(get_db), user=Depends(get_current_user)):
    if not body.profile_id and not body.inline_person:
        raise HTTPException(status_code=422, detail="Provide profile_id or inline_person")
    return NumerologyOut(number=5, ruling_planet="Mercury", details={"sample": True})

@router.get("/panchangam", response_model=PanchangamOut)
def panchangam(date: str = Query(...), lat: float = Query(...), lon: float = Query(...), tz: str = Query(...), db=Depends(get_db)):
    return PanchangamOut(date=date, lat=lat, lon=lon, tz=tz, periods={"rahukalam": "10:30-12:00"})

@router.post("/horoscope/daily")
def daily_horoscope(body: DailyHoroscopeIn, db=Depends(get_db), user=Depends(get_current_user)):
    return {"profile_id": body.profile_id, "advice": "Good day for decisions."}

@router.post("/tarot", response_model=TarotOut)
def tarot(body: TarotIn, db=Depends(get_db), user=Depends(get_current_user)):
    return TarotOut(spread=["The Sun","The Star","The Magician"], interpretation="Positive momentum, clarity, skill.")
