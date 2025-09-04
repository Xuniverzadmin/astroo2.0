from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from .common import UserOut, ProfileSummary

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: Optional[str] = None

class LoginIn(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str = Field(min_length=8, max_length=128)

class OTPStartIn(BaseModel):
    phone: str

class OTPVerifyIn(BaseModel):
    phone: str
    code: str = Field(min_length=4, max_length=8)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeOut(BaseModel):
    user: UserOut
    profiles: list[ProfileSummary] = []
