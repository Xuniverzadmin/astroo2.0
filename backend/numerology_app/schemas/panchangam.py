from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class PanchangamQuery(BaseModel):
    date: date
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    tz: Optional[str] = None

class PanchangamOut(BaseModel):
    sunrise: str
    sunset: str
    rahukaalam: str
    yamagandam: str
    gulikai: str
    tithi: str
    nakshatra: str
    yoga: str
    karana: str
