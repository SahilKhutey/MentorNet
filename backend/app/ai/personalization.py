import random
from typing import List, Dict, Any

def personalize_results(ranked_profiles, user_id, user_interests=None):
    if not user_id:
        return format_results(ranked_profiles)

    boosted = []
    interests_set = set(user_interests or [])

    for profile, score in ranked_profiles:
        profile_tags = [t.name for t in profile.tags]
        
        # 1. Interest Match Boosting
        # We give a higher weight to users who share specific tags with you
        match_count = len(interests_set.intersection(profile_tags))
        interest_boost = min(match_count * 0.08, 0.3) # Max 30% boost
        
        # 2. Discovery Factor (to avoid filter bubbles)
        # Adds a small random noise to allow for serendipitous discovery
        discovery_factor = random.uniform(0, 0.05)
        
        # 3. Final Calculation
        final_score = score + interest_boost + discovery_factor
        boosted.append((profile, final_score, match_count))

    boosted.sort(key=lambda x: x[1], reverse=True)

    return format_results(boosted)


def format_results(ranked):
    results = []

    for item in ranked:
        if len(item) == 3:
            p, score, match_count = item
        else:
            p, score = item
            match_count = 0
            
        results.append({
            "id": p.id,
            "name": p.full_name,
            "field": p.primary_field,
            "score": round(score, 4),
            "tags": [t.name for t in p.tags],
            "why": generate_explanation(p, match_count)
        })

    return results


def generate_explanation(profile, match_count=0):
    if match_count > 2:
        return f"Top match: High overlap with your {profile.primary_field} interests."
    elif match_count > 0:
        return f"Recommended based on your specific interest in {profile.primary_field}."
    else:
        return f"Discover new insights in {profile.primary_field} with this expert."
