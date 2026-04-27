from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.profile import Profile
from app.models.tag import Tag
from app.ai.search_engine import semantic_search
from app.ai.ranking_engine import rank_profiles
from app.ai.personalization import personalize_results

def hybrid_search(
    db: Session,
    query: str,
    user_id: Optional[int] = None,
    field: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 10
):
    # Step 1: Semantic Search (vector) - get larger candidate pool
    semantic_results = semantic_search(query, k=50)
    profile_ids = [r["profile_id"] for r in semantic_results]

    # Step 2: DB Filtering
    db_query = db.query(Profile).filter(Profile.id.in_(profile_ids))

    if field:
        db_query = db_query.filter(Profile.primary_field.ilike(f"%{field}%"))

    if tags:
        db_query = db_query.join(Profile.tags).filter(Tag.name.in_(tags))

    profiles = db_query.all()

    # Step 3: Multi-factor Ranking
    from app.models.availability import Availability
    from datetime import datetime
    
    # Pre-fetch availability counts for the candidate pool
    availability_map = {}
    for p in profiles:
        count = db.query(Availability).filter(
            Availability.mentor_id == p.user_id,
            Availability.start_time > datetime.utcnow()
        ).count()
        availability_map[p.id] = count

    # Step 3: Multi-factor Ranking
    ranked_tuples = rank_profiles(profiles, semantic_results, query, db=db)
    
    # Add availability boost and convert to objects for personalization
    final_ranked = []
    for p, score in ranked_tuples:
        avail_count = availability_map.get(p.id, 0)
        final_score = score
        is_available = False
        
        if avail_count > 0:
            final_score += 0.5 # Boost for being "Bookable" (normalized)
            is_available = True
        
        # We keep the profile object and the new score
        final_ranked.append((p, final_score))

    # Step 4: Personalization
    user_interests = []
    if user_id:
        from app.services.preference_service import PreferenceService
        pref_service = PreferenceService(db)
        user_interests = pref_service.get_user_interests(user_id)

    personalized = personalize_results(final_ranked, user_id, user_interests)

    return personalized[:limit]
