from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.models.session import Session as MentorshipSession
from app.ai.sentiment_analyzer import analyze_sentiment

def submit_feedback(db: Session, session_id: int, rating: float, review: str):
    session = db.query(MentorshipSession).filter(MentorshipSession.id == session_id).first()

    if not session:
        raise Exception("Mentorship session not found")

    # AI Intelligence: Analyze sentiment of the review
    sentiment = analyze_sentiment(review)

    feedback = Feedback(
        session_id=session_id,
        rating=rating,
        review=review,
        sentiment_score=sentiment,
        mentor_id=session.mentor_id,
        student_id=session.student_id
    )

    db.add(feedback)
    
    # Optional: Update mentor analytics immediately
    # update_mentor_analytics(db, session.mentor_id)
    
    db.commit()
    db.refresh(feedback)

    return feedback
