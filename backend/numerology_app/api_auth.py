# backend/numerology_app/api_auth.py
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import os, random

router = APIRouter()

OTP_TTL_MIN = 10
_memory_otp = {}  # { email: {"code": "123456", "exp": datetime} }

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    code: str

@router.post("/auth/request-otp")
async def request_otp(body: OTPRequest):
    code = f"{random.randint(0, 999999):06d}"
    _memory_otp[body.email] = {"code": code, "exp": datetime.utcnow() + timedelta(minutes=OTP_TTL_MIN)}
    # TODO: send email via SES/SendGrid/etc.
    return {"ok": True, "dev_code": code}  # remove dev_code in prod

@router.post("/auth/verify-otp")
async def verify_otp(body: OTPVerify, res: Response):
    rec = _memory_otp.get(body.email)
    if not rec or rec["exp"] < datetime.utcnow() or rec["code"] != body.code:
        raise HTTPException(400, "Invalid or expired OTP")
    # issue a **very simple** session cookie; replace with JWT in prod
    token = f"session:{body.email}"
    res.set_cookie("ao_session", token, httponly=True, secure=True, samesite="lax", max_age=60*60*24*30)
    return {"ok": True}
