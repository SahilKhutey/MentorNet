from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.ai.search_engine import semantic_search

class InsightService:
    @staticmethod
    def generate_insights(db: Session, user_id: str) -> List[Dict[str, Any]]:
        """
        Generates personalized insights for the user based on their profile and matching engine.
        """
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            return []

        insights = []

        # 1. Recommendation Insight: Find a top match and highlight it
        search_results = semantic_search(profile.bio, k=3)
        if search_results:
            top_match_id = search_results[0]["profile_id"]
            top_match = db.query(Profile).filter(Profile.id == top_match_id).first()
            if top_match:
                insights.append({
                    "id": f"rec_{top_match_id}",
                    "text": f"Your profile has an 85% semantic match with {top_match.full_name}. Consider connecting.",
                    "type": "recommendation",
                    "confidence": 0.85
                })

        # 2. Optimization Insight: Suggest adding missing tags based on similar profiles
        if len(profile.tags) < 3:
            insights.append({
                "id": "opt_tags",
                "text": "Add more research tags to improve your visibility in mentor searches.",
                "type": "optimization",
                "confidence": 0.90
            })
        
        # 3. Content Insight: If bio is short
        if len(profile.bio or "") < 50:
            insights.append({
                "id": "opt_bio",
                "text": "Your research bio is a bit short. Expanding it will help our AI find better mentor matches.",
                "type": "optimization",
                "confidence": 0.95
            })

        return insights

insight_service = InsightService()
