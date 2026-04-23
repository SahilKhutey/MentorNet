from sqlalchemy.orm import Session
from app.models.recommendation import Recommendation
from app.ai.recommendation_engine import generate_recommendations
from app.ai.personalization import format_results

def update_user_recommendations(db: Session, user_id: int):
    """
    Computes fresh recommendations and persists them to the cache table.
    This can be triggered by profile updates or background jobs.
    """
    from app.models.profile import Profile

    user_profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if not user_profile:
        return []

    # Generate Top-20 ranked mentors
    ranked = generate_recommendations(user_profile, db)

    # Atomic-like update: Clear old recommendations for this user
    db.query(Recommendation).filter(Recommendation.user_id == user_id).delete()

    # Bulk insert new recommendations
    for profile, score in ranked:
        rec = Recommendation(
            user_id=user_id,
            mentor_id=profile.id,
            score=score
        )
        db.add(rec)

    db.commit()

    # Invalidate cache
    cache_manager.delete(f"feed_user_{user_id}")
    
    # Return formatted results for immediate UI feedback
    return format_results(ranked)

from app.core.cache import cache_manager

def get_dashboard_feed(db: Session, user_id: int):
    """
    Fetches the highest-ranked cached recommendations for the user dashboard.
    """
    cache_key = f"feed_user_{user_id}"
    cached_data = cache_manager.get(cache_key)
    if cached_data:
        return cached_data

    from app.models.profile import Profile

    # Fetch top 10 cached recommendations from DB
    recs = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.score.desc()).limit(10).all()

    if not recs:
        # Fallback: Trigger initial generation if none exist
        return update_user_recommendations(db, user_id)

    # Hydrate profiles from IDs
    profile_ids = [r.mentor_id for r in recs]
    profiles = db.query(Profile).filter(Profile.id.in_(profile_ids)).all()

    # Map back to sorted list to maintain score order
    profile_map = {p.id: p for p in profiles}
    
    feed = [
        {
            "id": p.id,
            "name": p.full_name,
            "field": p.primary_field,
            "tags": [t.name for t in p.tags],
            "score": r.score,
            "why": f"High match based on your interests in {p.primary_field}."
        }
        for r in recs if (p := profile_map.get(r.mentor_id))
    ]
    
    # Cache for 10 minutes
    cache_manager.set(cache_key, feed, expire=600)
    return feed
