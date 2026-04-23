from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.recommendation_service import (
    update_user_recommendations,
    get_dashboard_feed
)

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("/refresh")
def refresh_recommendations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Force a re-computation of the AI recommendation feed.
    """
    results = update_user_recommendations(db, int(user["sub"]))
    return results

@router.get("/feed")
def get_feed(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Returns the personalized recommendation feed for the dashboard.
    """
    return get_dashboard_feed(db, int(user["sub"]))
