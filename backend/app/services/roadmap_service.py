from sqlalchemy.orm import Session
from app.models.roadmap import Roadmap
from typing import List, Dict, Optional
import uuid

class RoadmapService:
    @staticmethod
    def get_user_roadmap(db: Session, user_id: str) -> Optional[Roadmap]:
        return db.query(Roadmap).filter(Roadmap.user_id == user_id).first()

    @staticmethod
    def create_default_roadmap(db: Session, user_id: str, title: str = "My Career Journey"):
        milestones = [
            {"id": "m1", "title": "Complete Profile & Bio", "status": "completed"},
            {"id": "m2", "title": "First Mentorship Session", "status": "pending"},
            {"id": "m3", "title": "Receive First 5-Star Feedback", "status": "pending"},
            {"id": "m4", "title": "Refer 3 Friends", "status": "pending"},
            {"id": "m5", "title": "Become a Verified Peer Mentor", "status": "pending"}
        ]
        
        roadmap = Roadmap(
            user_id=user_id,
            title=title,
            milestones=milestones
        )
        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)
        return roadmap

    @staticmethod
    def update_milestone(db: Session, user_id: str, milestone_id: str, status: str):
        roadmap = db.query(Roadmap).filter(Roadmap.user_id == user_id).first()
        if not roadmap:
            return None
        
        updated_milestones = []
        for m in roadmap.milestones:
            if m["id"] == milestone_id:
                m["status"] = status
                if status == "completed":
                    from datetime import datetime
                    m["completed_at"] = datetime.utcnow().isoformat()
            updated_milestones.append(m)
        
        roadmap.milestones = updated_milestones
        db.commit()
        db.refresh(roadmap)
        return roadmap

roadmap_service = RoadmapService()
