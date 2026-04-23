from app.models.profile import Profile
from typing import List

def generate_match_explanation(student: Profile, mentor: Profile) -> str:
    """
    Generates a human-readable explanation for why a mentor was matched.
    """
    s_tags = {t.name.lower() for t in student.tags}
    m_tags = {t.name.lower() for t in mentor.tags}
    
    overlap = s_tags.intersection(m_tags)
    
    explanation = f"Matched based on shared expertise in {', '.join(list(overlap)[:2])}. "
    
    if student.primary_field == mentor.primary_field:
        explanation += f"Both are active in the {mentor.primary_field} domain. "
        
    if mentor.profile_score > 80:
        explanation += "This mentor is a top contributor in their field."
        
    return explanation or "Matched based on cross-disciplinary research potential."
