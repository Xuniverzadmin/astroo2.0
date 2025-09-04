from pydantic import BaseModel, Field
from typing import Optional

class ProfileCreate(BaseModel):
    name: str = Field(..., max_length=80)
    dob: str
    tob: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None
    relation: Optional[str] = None

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=80)
    dob: Optional[str] = None
    tob: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None
    relation: Optional[str] = None

class ProfileOut(BaseModel):
    id: int
    name: str
    dob: str
    tob: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None
    relation: Optional[str] = None
