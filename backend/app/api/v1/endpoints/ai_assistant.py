from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.models.profile import Profile
from app.ai.assistant import draft_connection_request, summarize_mentor_profile

from app.services.ai_assistant_service import ai_assistant_service
from pydantic import BaseModel

class AssistantQuery(BaseModel):
    query: str

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])

@router.post("/ask")
def ask_assistant(
    data: AssistantQuery,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Elite Research Assistant conversational endpoint.
    """
    user_id = str(user["sub"])
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    
    context = {
        "user_id": user_id,
        "full_name": profile.full_name if profile else "Researcher",
        "field": profile.primary_field if profile else "Academic"
    }
    
    response = ai_assistant_service.get_response(data.query, context, db)
    return {"response": response}

@router.get("/draft-request/{mentor_id}")
def get_draft_request(mentor_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    student_id = str(user["sub"])
    
    student = db.query(Profile).filter(Profile.user_id == student_id).first()
    mentor = db.query(Profile).filter(Profile.id == mentor_id).first()
    
    if not student or not mentor:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    return {"draft": draft_connection_request(student, mentor)}

@router.get("/summarize/{mentor_id}")
def get_mentor_summary(mentor_id: str, db: Session = Depends(get_db)):
    mentor = db.query(Profile).filter(Profile.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
        
    return {"summary": summarize_mentor_profile(mentor)}
