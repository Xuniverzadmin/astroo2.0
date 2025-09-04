from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.auth import RegisterIn, LoginIn, OTPStartIn, OTPVerifyIn, TokenOut, MeOut
from ..schemas.common import UserOut, ProfileSummary
from ..security import create_jwt, hash_password, verify_password
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut, status_code=201)
def register_user(body: RegisterIn, db=Depends(get_db)):
    # TODO: check if user exists, insert with hash_password(body.password)
    user_id = 1
    token = create_jwt(str(user_id))
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login_user(body: LoginIn, db=Depends(get_db)):
    # TODO: lookup by email/phone; verify_password
    ok = True
    if not ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user_id = 1
    return TokenOut(access_token=create_jwt(str(user_id)))

@router.post("/otp/start", status_code=202)
def otp_start(body: OTPStartIn, db=Depends(get_db)):
    # TODO: send OTP
    return {"message": "OTP sent"}

@router.post("/otp/verify", response_model=TokenOut)
def otp_verify(body: OTPVerifyIn, db=Depends(get_db)):
    # TODO: verify OTP
    user_id = 1
    return TokenOut(access_token=create_jwt(str(user_id)))

@router.get("/me", response_model=MeOut)
def get_me(current=Depends(get_current_user), db=Depends(get_db)):
    user = UserOut(id=int(current["id"]) if isinstance(current["id"], int) else 1,
                   email="demo@example.com", phone="9999999999")
    profiles = [ProfileSummary(id=1, name="You", dob="1990-01-01")]
    return MeOut(user=user, profiles=profiles)
