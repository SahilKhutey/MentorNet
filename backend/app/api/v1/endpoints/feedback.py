from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.feedback_service import submit_feedback
from app.services.analytics_service import update_mentor_analytics

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/")
def give_feedback(
    session_id: int, 
    rating: float, 
    review: str, 
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Submits feedback for a completed session and re-calculates mentor analytics.
    """
    try:
        fb = submit_feedback(db, session_id, rating, review)
        # Auto-update the mentor's aggregate analytics
        update_mentor_analytics(db, fb.mentor_id)
        return {"status": "feedback submitted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
