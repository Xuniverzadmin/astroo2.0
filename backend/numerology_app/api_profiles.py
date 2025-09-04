# backend/numerology_app/api_profiles.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

router = APIRouter()
_db_profiles = {}  # {id: {...}}

class Profile(BaseModel):
    id: str
    name: str
    dob: str
    place: str | None = None
    lat: float | None = None
    lon: float | None = None
    relation: str | None = None

class ProfileCreate(BaseModel):
    name: str
    dob: str
    place: str | None = None
    lat: float | None = None
    lon: float | None = None
    relation: str | None = None

@router.get("/profiles", response_model=List[Profile])
async def list_profiles():
    return list(_db_profiles.values())

@router.post("/profiles", response_model=Profile)
async def create_profile(body: ProfileCreate):
    pid = uuid4().hex
    prof = Profile(id=pid, **body.model_dump())
    _db_profiles[pid] = prof.model_dump()
    return prof

@router.delete("/profiles/{pid}")
async def delete_profile(pid: str):
    if pid in _db_profiles:
        del _db_profiles[pid]
        return {"ok": True}
    raise HTTPException(404, "Not found")
@router.get("/profiles/{pid}", response_model=Profile)
async def get_profile(pid: str):
    if pid in _db_profiles:
        return Profile(**_db_profiles[pid])
    raise HTTPException(404, "Not found")   