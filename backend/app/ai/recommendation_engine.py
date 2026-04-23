from app.ai.embedding import generate_embedding
from app.ai.vector_db.index_manager import faiss_store
from app.ai.ranking_engine import rank_profiles

def generate_recommendations(user_profile, db, limit=20):
    """
    Core AI logic: Convert user profile to embedding, find similar mentors, 
    and rank them based on multi-factor scores.
    """
    # Step 1: Build user semantic context
    # We focus on their primary field and bio to find compatible mentors
    text = f"{user_profile.primary_field} {user_profile.bio}"
    user_embedding = generate_embedding(text)

    # Step 2: Retrieve Top-K candidates from FAISS
    # We retrieve 100 to ensure we have enough diversity after filtering
    results = faiss_store.search(user_embedding, k=100)
    profile_ids = [r["profile_id"] for r in results]

    from app.models.profile import Profile
    from app.models.user import User
    from app.core.constants import UserRole
    
    # Fetch actual mentor profiles from DB
    # We filter for MENTOR role specifically for discovery
    mentors = db.query(Profile).join(User).filter(
        Profile.id.in_(profile_ids),
        User.role == UserRole.MENTOR
    ).all()

    # Step 3: Apply the multi-factor Ranking Engine (re-ranking)
    ranked = rank_profiles(mentors, results, text)

    return ranked[:limit]
