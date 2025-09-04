from pydantic import BaseModel
from typing import Optional, Literal

class ChatMessage(BaseModel):
    role: Literal["system","user","assistant"]
    content: str

class ChatIn(BaseModel):
    messages: list[ChatMessage]
    profile_id: Optional[int] = None

class ChatOut(BaseModel):
    reply: str
