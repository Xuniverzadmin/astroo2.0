from fastapi import APIRouter, Depends, Header, Request
from ..schemas.store import ProductOut, OrderCreate, OrderOut, SubscriptionCreate, SubscriptionOut
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/store", tags=["store"])

@router.get("/products", response_model=list[ProductOut])
def list_products(db=Depends(get_db)):
    return [ProductOut(id=1, name="Daily Horoscope", price_cents=4999)]

@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(body: OrderCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return OrderOut(id=1, amount_cents=body.quantity*4999, currency="INR", payment_url="https://pay/link", status="pending")

@router.post("/subscriptions", response_model=SubscriptionOut, status_code=201)
def start_subscription(body: SubscriptionCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return SubscriptionOut(id=1, status="trialing")

@router.post("/webhooks/razorpay", status_code=202)
async def razorpay_webhook(request: Request, x_razorpay_signature: str | None = Header(None)):
    raw = await request.body()
    return {"message": "accepted"}

@router.post("/webhooks/stripe", status_code=202)
async def stripe_webhook(request: Request, stripe_signature: str | None = Header(None)):
    raw = await request.body()
    return {"message": "accepted"}
