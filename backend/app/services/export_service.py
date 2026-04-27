import json
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile
from app.models.booking import Booking
from app.models.session import Session as MentorshipSession
from app.models.feedback import Feedback
from app.models.roadmap import Roadmap
from app.models.notification import Notification

class ExportService:
    @staticmethod
    def generate_user_data_export(db: Session, user_id: str):
        """
        Gathers all user-related data for GDPR compliance export.
        """
        user = db.query(User).filter(User.id == user_id).first()
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        bookings = db.query(Booking).filter(Booking.student_id == user_id).all()
        sessions = db.query(MentorshipSession).filter(MentorshipSession.student_id == user_id).all()
        feedbacks = db.query(Feedback).filter(Feedback.student_id == user_id).all()
        roadmaps = db.query(Roadmap).filter(Roadmap.user_id == user_id).all()
        notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
        
        data = {
            "account": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "created_at": str(user.created_at)
            },
            "profile": {
                "full_name": profile.full_name if profile else None,
                "headline": profile.headline if profile else None,
                "primary_field": profile.primary_field if profile else None,
                "expertise": [tag.name for tag in profile.tags] if profile else []
            },
            "activity": {
                "bookings_count": len(bookings),
                "sessions_completed": len([s for s in sessions if s.status == "completed"]),
                "feedbacks_given": len(feedbacks),
                "roadmaps_active": len(roadmaps)
            },
            "notifications": [
                {"title": n.title, "message": n.message, "created_at": str(n.created_at)}
                for n in notifications
            ]
        }
        
        return data

export_service = ExportService()
