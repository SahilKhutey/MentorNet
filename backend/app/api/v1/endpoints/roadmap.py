from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.roadmap_service import roadmap_service
from app.schemas.profile_schema import ProfileResponse # We might need a roadmap schema later

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

@router.get("/")
def get_my_roadmap(db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_id = str(user["sub"])
    roadmap = roadmap_service.get_user_roadmap(db, user_id)
    if not roadmap:
        # Create a default one if it doesn't exist
        roadmap = roadmap_service.create_default_roadmap(db, user_id)
    return roadmap

@router.post("/milestone/{milestone_id}")
def complete_milestone(milestone_id: str, status: str = "completed", db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_id = str(user["sub"])
    roadmap = roadmap_service.update_milestone(db, user_id, milestone_id, status)
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return roadmap
