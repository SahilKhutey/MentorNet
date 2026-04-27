from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.analytics import MentorAnalytics
from app.models.profile import Profile
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

from app.core.dependencies import get_db, get_current_user
from app.models.feedback import Feedback
from app.models.session import Session as MentorshipSession
from app.models.ai_insight_event import AIInsightEvent
from pydantic import BaseModel

class AIEventCreate(BaseModel):
    insight_id: str
    action: str # 'view', 'apply', 'dismiss', 'click'
    confidence: float

@router.post("/ai/track")
def track_ai_event(
    event: AIEventCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Logs an interaction with an AI insight for analytics and model improvement.
    """
    new_event = AIInsightEvent(
        user_id=str(user["sub"]),
        insight_id=event.insight_id,
        action=event.action,
        confidence=event.confidence
    )
    db.add(new_event)
    db.commit()
    return {"status": "tracked"}

@router.get("/mentor/impact/{mentor_id}")
def get_mentor_impact(mentor_id: int, db: Session = Depends(get_db)):
    """
    Returns high-level impact metrics for a mentor.
    """
    data = db.query(MentorAnalytics).filter(MentorAnalytics.mentor_id == mentor_id).first()
    recent_reviews = db.query(Feedback).filter(Feedback.mentor_id == mentor_id).order_by(Feedback.created_at.desc()).limit(5).all()
    
    return {
        "metrics": data,
        "recent_vibe": [r.sentiment_score for r in recent_reviews if r.sentiment_score is not None],
        "highlight_reviews": [{"review": r.review, "rating": r.rating} for r in recent_reviews]
    }

@router.get("/student/growth")
def get_student_growth(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Calculates learning growth for the current student.
    """
    user_id = str(user["sub"])
    completed_sessions = db.query(MentorshipSession).filter(
        MentorshipSession.student_id == user_id,
        MentorshipSession.status == "completed"
    ).count()
    
    # We can expand this to check "skills" from session outcomes
    return {
        "completed_sessions": completed_sessions,
        "hours_mentored": completed_sessions * 1.5, # Assuming 1.5hr avg
        "growth_stage": "Pioneer" if completed_sessions > 10 else "Explorer"
    }

@router.get("/leaderboard")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """
    Returns the top mentors based on contribution scores.
    """
    top_mentors = db.query(MentorAnalytics).order_by(
        MentorAnalytics.contribution_score.desc()
    ).limit(limit).all()
    
    # Enrich with profile names
    results = []
    for m in top_mentors:
        profile = db.query(Profile).filter(Profile.user_id == m.mentor_id).first()
        results.append({
            "name": profile.full_name if profile else "Anonymous",
            "score": round(m.contribution_score, 2),
            "rating": m.avg_rating,
            "field": profile.primary_field if profile else "Researcher"
        })
    return results

@router.get("/referrals")
def get_referral_stats(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Returns the count and details of users referred by the current user.
    """
    user_id = str(user["sub"])
    referred_users = db.query(User).filter(User.referrer_id == user_id).all()
    
    return {
        "count": len(referred_users),
        "referred_users": [
            {"name": u.name, "created_at": u.created_at, "role": u.role}
            for u in referred_users
        ]
    }
