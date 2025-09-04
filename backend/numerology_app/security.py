import os, time, hmac, hashlib, base64
from typing import Optional, Any, Dict
from pydantic import BaseModel
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME")
JWT_ISSUER = os.getenv("JWT_ISSUER", "astrooverz")
JWT_TTL_SECONDS = int(os.getenv("JWT_TTL_SECONDS", "86400"))  # 24h

def hash_password(password: str) -> str:
    return PWD_CONTEXT.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return PWD_CONTEXT.verify(password, hashed)

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def _b64url_json(obj: Dict[str, Any]) -> str:
    import json
    return _b64url(json.dumps(obj, separators=(",", ":")).encode())

def create_jwt(sub: str, extra: Optional[dict] = None) -> str:
    now = int(time.time())
    payload = {
        "iss": JWT_ISSUER,
        "sub": sub,
        "iat": now,
        "exp": now + JWT_TTL_SECONDS,
        **(extra or {}),
    }
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url_json(header)
    p = _b64url_json(payload)
    to_sign = f"{h}.{p}".encode()
    sig = hmac.new(JWT_SECRET.encode(), to_sign, hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url(sig)}"

class DecodedJWT(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int

def decode_jwt(token: str) -> DecodedJWT:
    import json
    h_b64, p_b64, s_b64 = token.split(".")
    to_sign = f"{h_b64}.{p_b64}".encode()
    expected = hmac.new(JWT_SECRET.encode(), to_sign, hashlib.sha256).digest()
    got = base64.urlsafe_b64decode(s_b64 + "==")
    if not hmac.compare_digest(expected, got):
        raise ValueError("Invalid signature")
    payload = json.loads(base64.urlsafe_b64decode(p_b64 + "=="))
    now = int(time.time())
    if payload.get("exp", 0) < now:
        raise ValueError("Token expired")
    return DecodedJWT(**payload)
