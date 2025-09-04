from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

class APIMessage(BaseModel):
    message: str = Field(..., examples=["ok"])

class Paginated(BaseModel):
    total: int = 0
    page: int = 1
    page_size: int = 20

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    phone: Optional[str] = None

class ProfileSummary(BaseModel):
    id: int
    name: str
    dob: str
