def calculate_tag_similarity(query, profile):
    query_words = set(query.lower().split())
    tag_names = [t.name.lower() for t in profile.tags]
    if not tag_names: return 0
    
    tag_words = set(tag_names)
    intersection = query_words & tag_words
    union = query_words | tag_words
    # Jaccard Similarity (IoU)
    return len(intersection) / len(union) if union else 0


def profile_completeness(profile):
    score = 0
    if profile.bio: score += 1
    if profile.primary_field: score += 1
    if profile.institution: score += 1
    if profile.tags: score += 1
    return score / 4


def calculate_expertise_score(profile):
    """Boost based on publications and citations."""
    pub_count = len(profile.publications)
    total_citations = sum(p.citation_count for p in profile.publications)
    
    # Logarithmic scaling to prevent outliers from dominating
    import math
    pub_score = math.log1p(pub_count) / 5  # Normalized approx 0-1 for common ranges
    cite_score = math.log1p(total_citations) / 10
    
    return min(1.0, pub_score + cite_score)


def calculate_experience_score(profile):
    """Boost based on number of professional experiences."""
    exp_count = len(profile.experience)
    return min(1.0, exp_count / 5)


from sqlalchemy.orm import Session

def add_analytics_score(profile, db: Session):
    from app.models.analytics import MentorAnalytics
    
    analytics = db.query(MentorAnalytics).filter(
        MentorAnalytics.mentor_id == profile.id
    ).first()

    if not analytics:
        return 0.3

    return (
        0.5 * (analytics.avg_rating / 5) + 
        0.5 * analytics.success_rate
    )

def rank_profiles(profiles, semantic_results, query, db: Session = None):
    score_map = {r["profile_id"]: r["score"] for r in semantic_results}
    ranked = []

    for p in profiles:
        # Normalize distance (smaller L2 distance means better match)
        semantic_score = 1 / (1 + score_map.get(p.id, 1))

        tag_score = calculate_tag_similarity(query, p)
        completeness = profile_completeness(p)
        expertise = calculate_expertise_score(p)
        experience = calculate_experience_score(p)
        
        # Multi-factor Intelligence Scoring
        final_score = (
            0.40 * semantic_score +
            0.15 * tag_score +
            0.10 * completeness +
            0.15 * expertise +
            0.10 * experience +
            0.10 * 0.5  # placeholder activity
        )

        # Intelligence Loop: Boost by mentor performance
        if db:
            analytics_score = add_analytics_score(p, db)
            final_score += 0.2 * analytics_score
            # Normalize to keep in roughly [0, 1] range
            final_score /= 1.2

        ranked.append((p, final_score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
