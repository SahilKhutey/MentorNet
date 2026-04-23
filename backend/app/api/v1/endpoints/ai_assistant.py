from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.models.profile import Profile
from app.ai.assistant import draft_connection_request, summarize_mentor_profile

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

@router.get("/draft-request/{mentor_id}")
def get_draft_request(mentor_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    student_id = int(user["sub"])
    
    student = db.query(Profile).filter(Profile.user_id == student_id).first()
    mentor = db.query(Profile).filter(Profile.id == mentor_id).first()
    
    if not student or not mentor:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    return {"draft": draft_connection_request(student, mentor)}

@router.get("/summarize/{mentor_id}")
def get_mentor_summary(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.query(Profile).filter(Profile.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
        
    return {"summary": summarize_mentor_profile(mentor)}
