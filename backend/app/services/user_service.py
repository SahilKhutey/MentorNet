from sqlalchemy.orm import Session
from app.models.user import User, RefreshToken
from app.models.profile import Profile
from app.models.booking import Booking
from app.models.feedback import Feedback
from app.models.session import Session as MentorSession

def delete_user_data(db: Session, user_id: str):
    """
    Securely delete all user data (Right to be Forgotten).
    Ensures all related records are purged or anonymized.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    # 1. Purge Sessions & Bookings
    db.query(MentorSession).filter((MentorSession.mentor_id == user_id) | (MentorSession.student_id == user_id)).delete()
    db.query(Booking).filter((Booking.mentor_id == user_id) | (Booking.student_id == user_id)).delete()
    
    # 2. Purge Feedback
    db.query(Feedback).filter((Feedback.mentor_id == user_id) | (Feedback.student_id == user_id)).delete()
    
    # 3. Purge Profile & Tokens
    db.query(Profile).filter(Profile.user_id == user_id).delete()
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    
    # 4. Delete User
    db.delete(user)
    db.commit()
    return True

def get_user_data_export(db: Session, user_id: str):
    """
    Retrieve all user data for portability (GDPR).
    """
    from app.services.export_service import export_service
    # We expect user_id to be a string from the token (sub claim)
    return export_service.generate_user_data_export(db, str(user_id))
