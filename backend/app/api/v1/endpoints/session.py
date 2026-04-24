from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.core.dependencies import get_db, get_current_user
from app.models.session import Session
from app.models.feedback import Feedback
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/sessions", tags=["Sessions"])

class FeedbackCreate(BaseModel):
    session_id: str
    rating: int
    review: Optional[str] = None

@router.get("/")
def get_my_sessions(db: DBSession = Depends(get_db), user_id: str = Depends(get_current_user)):
    return db.query(Session).filter(
        (Session.mentor_id == user_id) | (Session.student_id == user_id)
    ).all()

@router.get("/{session_id}")
def get_session(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/feedback")
def give_feedback(
    data: FeedbackCreate, 
    db: DBSession = Depends(get_db), 
    user_id: str = Depends(get_current_user)
):
    # Verify session exists and user was part of it
    session = db.query(Session).filter(Session.id == data.session_id).first()
    if not session or (session.mentor_id != user_id and session.student_id != user_id):
        raise HTTPException(status_code=403, detail="Not authorized to give feedback for this session")
    
    feedback = Feedback(
        session_id=data.session_id,
        mentor_id=session.mentor_id,
        student_id=session.student_id,
        rating=data.rating,
        review=data.review
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"status": "feedback recorded"}
