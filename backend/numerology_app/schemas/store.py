from pydantic import BaseModel, Field
from typing import Optional, Literal

Status = Literal['active','incomplete','past_due','canceled','paused','trialing']

class ProductOut(BaseModel):
    id: int
    name: str
    price_cents: int
    currency: str = "INR"
    active: bool = True

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=100)
    gateway: Literal["razorpay","stripe"]

class OrderOut(BaseModel):
    id: int
    amount_cents: int
    currency: str
    payment_url: Optional[str] = None
    status: str

class SubscriptionCreate(BaseModel):
    product_id: int
    gateway: Literal["razorpay","stripe"]

class SubscriptionOut(BaseModel):
    id: int
    status: Status
    current_period_start: Optional[str] = None
    current_period_end: Optional[str] = None
