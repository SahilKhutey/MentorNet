from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.feedback import Feedback
from app.models.analytics import MentorAnalytics

def update_mentor_analytics(db: Session, mentor_id: int):
    # Calculate stats from feedback
    stats = db.query(
        func.avg(Feedback.rating).label("avg_rating"),
        func.avg(Feedback.sentiment_score).label("avg_sentiment"),
        func.count(Feedback.id).label("total_feedback")
    ).filter(Feedback.mentor_id == mentor_id).first()

    if not stats.total_feedback:
        return

    # Update or create analytics record
    analytics = db.query(MentorAnalytics).filter(MentorAnalytics.mentor_id == mentor_id).first()
    if not analytics:
        analytics = MentorAnalytics(mentor_id=mentor_id)
        db.add(analytics)

    analytics.avg_rating = float(stats.avg_rating or 0)
    analytics.sentiment_avg = float(stats.avg_sentiment or 0)
    analytics.total_sessions = int(stats.total_feedback)
    
    # 1. Success rate calculation
    positive_feedback = db.query(Feedback).filter(
        Feedback.mentor_id == mentor_id,
        Feedback.rating >= 4
    ).count()
    analytics.success_rate = positive_feedback / stats.total_feedback if stats.total_feedback else 0

    # 2. Advanced Contribution Score: (Sessions) * (Rating/5) * (1 + Sentiment)
    # Rewards both volume and high-vibe interactions
    vibe_multiplier = 1.0 + analytics.sentiment_avg
    rating_weight = analytics.avg_rating / 5.0
    analytics.contribution_score = (analytics.total_sessions * rating_weight * vibe_multiplier)
    
    db.commit()
    return analytics
