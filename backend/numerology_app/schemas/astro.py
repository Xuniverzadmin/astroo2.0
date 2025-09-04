from pydantic import BaseModel, Field
from typing import Optional

class InlinePerson(BaseModel):
    name: str
    dob: str
    tob: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None

class NumerologyIn(BaseModel):
    profile_id: Optional[int] = None
    inline_person: Optional[InlinePerson] = None
    text: Optional[str] = Field(default=None, description="Optional name/text to analyse")

class NumerologyOut(BaseModel):
    number: int
    ruling_planet: str
    details: dict

class PanchangamOut(BaseModel):
    date: str
    lat: float
    lon: float
    tz: str
    periods: dict

class DailyHoroscopeIn(BaseModel):
    profile_id: int

class TarotIn(BaseModel):
    profile_id: int
    question: str

class TarotOut(BaseModel):
    spread: list[str]
    interpretation: str
