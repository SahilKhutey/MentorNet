from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.ai.search_engine import semantic_search
from app.ai.explainability import generate_match_explanation

def search_profiles_semantic(db: Session, query: str, current_user_id: int = None, limit: int = 10):
    from app.models.user import User
    from app.core.constants import UserRole
    
    # Fetch student profile for explanation if available
    student = None
    if current_user_id:
        student = db.query(Profile).filter(Profile.user_id == current_user_id).first()

    # Retrieve candidates
    results = semantic_search(query, k=limit * 3)
    profile_ids = [r["profile_id"] for r in results]

    from sqlalchemy.orm import joinedload
    profiles = db.query(Profile).options(
        joinedload(Profile.tags),
        joinedload(Profile.user)
    ).join(User).filter(
        Profile.id.in_(profile_ids),
        User.role == UserRole.MENTOR
    ).all()

    score_map = {r["profile_id"]: r["score"] for r in results}
    profiles.sort(key=lambda x: score_map.get(x.id, 999))

    response = []
    for p in profiles[:limit]:
        dist = score_map.get(p.id)
        similarity = 1 / (1 + dist) if dist is not None else 0
        
        # AI Insight: Why this match?
        why = generate_match_explanation(student, p) if student else f"Semantic overlap in {p.primary_field}."

        response.append({
            "id": p.id,
            "name": p.full_name,
            "field": p.primary_field,
            "tags": [t.name for t in p.tags],
            "score": round(float(similarity), 4),
            "why": why
        })

    return response
