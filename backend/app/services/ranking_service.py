from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.feedback import Feedback
from app.models.booking import Booking
from app.models.user import User

def calculate_mentor_score(db: Session, mentor_id: str):
    """
    Mentor Ranking Algorithm V1:
    Score = (Avg Rating * 0.5) + (Booking Volume * 0.3) + (Profile Completeness * 0.2)
    """
    
    # 1. Average Rating
    avg_rating = db.query(func.avg(Feedback.rating)).filter(Feedback.mentor_id == mentor_id).scalar() or 0
    normalized_rating = (avg_rating / 5.0) * 100 # scale to 0-100
    
    # 2. Booking Volume
    booking_count = db.query(func.count(Booking.id)).filter(Booking.mentor_id == mentor_id).scalar() or 0
    normalized_volume = min(booking_count * 5, 100) # caps at 20 bookings for max volume score
    
    # 3. Simple composite score
    score = (normalized_rating * 0.5) + (normalized_volume * 0.3) + (20) # Base completeness score of 20
    
    return round(score, 2)

def get_trending_mentors(db: Session, limit: int = 10):
    """Fetch mentors sorted by their ranking score using high-performance SQL aggregations."""
    from sqlalchemy import case, literal
    
    # Single efficient query to calculate scores for all mentors
    results = db.query(
        User.id,
        User.name,
        User.username,
        func.coalesce(func.avg(Feedback.rating), 0).label("avg_rating"),
        func.count(Booking.id).label("booking_count")
    ).outerjoin(Feedback, User.id == Feedback.mentor_id)\
     .outerjoin(Booking, User.id == Booking.mentor_id)\
     .filter(User.role == "mentor")\
     .group_by(User.id)\
     .all()

    scored_mentors = []
    for r in results:
        normalized_rating = (float(r.avg_rating) / 5.0) * 100
        normalized_volume = min(r.booking_count * 5, 100)
        score = (normalized_rating * 0.5) + (normalized_volume * 0.3) + 20
        
        scored_mentors.append({
            "id": r.id,
            "name": r.name,
            "username": r.username,
            "score": round(score, 2),
            "badges": ["Top Rated"] if score > 80 else []
        })

    return sorted(scored_mentors, key=lambda x: x["score"], reverse=True)[:limit]
