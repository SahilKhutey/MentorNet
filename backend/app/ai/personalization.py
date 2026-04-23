def personalize_results(ranked_profiles, user_id):
    if not user_id:
        return format_results(ranked_profiles)

    # TODO: fetch user preferences from DB to drive real personalization
    boosted = []

    for profile, score in ranked_profiles:
        boost = 0

        # Example logic: Boost profiles with "AI" tags if we know user likes AI
        if "AI" in [t.name for t in profile.tags]:
            boost += 0.1

        final_score = score + boost
        boosted.append((profile, final_score))

    boosted.sort(key=lambda x: x[1], reverse=True)

    return format_results(boosted)


def format_results(ranked):
    results = []

    for p, score in ranked:
        results.append({
            "id": p.id,
            "name": p.full_name,
            "field": p.primary_field,
            "score": round(score, 4),
            "tags": [t.name for t in p.tags],
            "why": generate_explanation(p)
        })

    return results


def generate_explanation(profile):
    return f"Matched on {profile.primary_field} and relevant expertise."
