from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.profiles import ProfileCreate, ProfileUpdate, ProfileOut
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("", response_model=ProfileOut, status_code=201)
def create_profile(body: ProfileCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return ProfileOut(id=1, **body.dict())

@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    if profile_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return ProfileOut(id=1, name="You", dob="1990-01-01")

@router.patch("/{profile_id}", response_model=ProfileOut)
def update_profile(profile_id: int, body: ProfileUpdate, db=Depends(get_db), user=Depends(get_current_user)):
    return ProfileOut(id=profile_id, name=body.name or "You", dob=body.dob or "1990-01-01")

@router.delete("/{profile_id}", status_code=204)
def delete_profile(profile_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return
