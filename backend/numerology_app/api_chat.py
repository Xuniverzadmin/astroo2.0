# backend/numerology_app/api_chat.py
from __future__ import annotations
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",          # adjust if you prefer another model
            messages=[m.model_dump() for m in req.messages],
            temperature=0.7,
        )
        return {"reply": r.choices[0].message.content}
    except Exception as e:
        # Surface a clean error to the client (also log server-side if you prefer)
        raise HTTPException(500, f"LLM error: {e}")
