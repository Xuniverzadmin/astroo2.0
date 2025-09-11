# backend/numerology_app/api_llm.py
from __future__ import annotations
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PromptIn(BaseModel):
    prompt: str
    system: str | None = "You are a helpful assistant."

@router.post("/ask")
def ask_astrooverz(body: PromptIn):
    """Ask Astrooverz - simplified endpoint for the chat widget."""
    try:
        system_prompt = "You are Astrooverz, a knowledgeable Vedic astrology and numerology guide. Provide helpful, accurate information about astrology, numerology, and life guidance based on ancient wisdom."
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": body.prompt},
            ],
            temperature=0.7,
        )
        return {"reply": r.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"LLM error: {e}")

@router.post("/llm/complete")
def llm_complete(body: PromptIn):
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": body.system or "You are a helpful assistant."},
                {"role": "user", "content": body.prompt},
            ],
            temperature=0.7,
        )
        return {"reply": r.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"LLM error: {e}")
