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
