from fastapi import APIRouter, Depends
from ..schemas.llm import ChatIn, ChatOut
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/chat", response_model=ChatOut)
def chat(body: ChatIn, db=Depends(get_db), user=Depends(get_current_user)):
    reply = "This is a stubbed reply."
    return ChatOut(reply=reply)
