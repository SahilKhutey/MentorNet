from typing import List
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile

class PreferenceService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_interests(self, user_id: str) -> List[str]:
        """
        Retrieves a list of tags representing the user's current interests.
        In a real system, this would analyze recent searches, interactions, and profile data.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return []
        
        # Combine profile tags with implicit interests (e.g., from recent searches)
        # For now, we use the profile tags as the primary source.
        return [tag.name for tag in user.profile.tags]

    def calculate_boost_score(self, profile_tags: List[str], user_interests: List[str]) -> float:
        """
        Calculates a boost score based on the intersection of profile tags and user interests.
        """
        if not user_interests:
            return 0.0
        
        intersection = set(profile_tags) & set(user_interests)
        # Simple linear boost: 0.1 for every matching tag, max 0.5
        return min(len(intersection) * 0.1, 0.5)

preference_service = PreferenceService
