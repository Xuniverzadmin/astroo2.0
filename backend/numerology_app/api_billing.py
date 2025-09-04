# backend/numerology_app/api_billing.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, stripe, uuid

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class CreateCheckout(BaseModel):
    plan: str  # "pro" | "premium"

PRICES = {
    "pro":     {"name":"Pro Monthly", "stripe_price":"price_XXXX", "amount":29900, "currency":"inr"},
    "premium": {"name":"Premium Monthly", "stripe_price":"price_YYYY", "amount":69900, "currency":"inr"},
}

@router.post("/billing/stripe/checkout")
async def stripe_checkout(body: CreateCheckout):
    p = PRICES.get(body.plan)
    if not p:
        raise HTTPException(400, "Invalid plan")
    try:
        sess = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": p["stripe_price"], "quantity": 1}],
            success_url=os.getenv("SUCCESS_URL", "https://astrooverz.com/?p=success"),
            cancel_url=os.getenv("CANCEL_URL", "https://astrooverz.com/?p=cancel"),
        )
        return {"url": sess.url}
    except Exception as e:
        raise HTTPException(500, str(e))
