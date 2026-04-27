from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.chat_service import get_chat_history, get_recent_chats

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/history/{target_id}")
def chat_history(target_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return get_chat_history(db, str(user["sub"]), target_id)

@router.get("/recent")
def recent_conversations(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return get_recent_chats(db, str(user["sub"]))
