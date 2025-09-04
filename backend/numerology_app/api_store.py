# backend/numerology_app/api_store.py
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .db import get_db
from .models import Item

router = APIRouter()

class ItemIn(BaseModel):
    title: str
    description: str | None = None

class ItemOut(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        from_attributes = True

@router.get("/store/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).order_by(Item.id.desc()).all()

@router.post("/store/items", response_model=ItemOut)
def create_item(body: ItemIn, db: Session = Depends(get_db)):
    obj = Item(title=body.title, description=body.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/store/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(Item, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj

@router.delete("/store/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(Item, item_id)
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}
