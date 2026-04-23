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
    ranked = rank_profiles(profiles, semantic_results, query, db=db)

    # Step 4: Personalization
    personalized = personalize_results(ranked, user_id)

    return personalized[:limit]
