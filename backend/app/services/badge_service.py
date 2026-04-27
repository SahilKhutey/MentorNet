from sqlalchemy.orm import Session
from app.models.badge import Badge
from app.models.user import User
from app.models.analytics import MentorAnalytics

class BadgeService:
    @staticmethod
    def check_and_award_badges(db: Session, user_id: str):
        """
        Logic to automatically award badges based on mentor performance.
        """
        user = db.query(User).filter(User.id == user_id).first()
        analytics = db.query(MentorAnalytics).filter(MentorAnalytics.mentor_id == user_id).first()
        
        if not analytics:
            return []

        new_badges = []
        
        # 1. "Elite Connector" - 50+ sessions
        if analytics.sessions_completed >= 50:
            badge = db.query(Badge).filter(Badge.name == "Elite Connector").first()
            if badge and badge not in user.badges:
                user.badges.append(badge)
                new_badges.append(badge)

        # 2. "Top Rated" - 4.9+ rating
        if analytics.avg_rating >= 4.9:
            badge = db.query(Badge).filter(Badge.name == "Top Rated").first()
            if badge and badge not in user.badges:
                user.badges.append(badge)
                new_badges.append(badge)

        db.commit()
        return new_badges

badge_service = BadgeService()
