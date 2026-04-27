from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.recommendation_service import (
    update_user_recommendations,
    get_dashboard_feed
)
from app.services.insight_service import insight_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/insights")
def get_insights(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Returns AI-generated insights and optimizations for the user.
    """
    return insight_service.generate_insights(db, str(user["sub"]))

@router.post("/refresh")
def refresh_recommendations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Force a re-computation of the AI recommendation feed.
    """
    results = update_user_recommendations(db, str(user["sub"]))
    return results

@router.get("/feed")
def get_feed(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Returns the personalized recommendation feed for the dashboard.
    """
    return get_dashboard_feed(db, str(user["sub"]))
