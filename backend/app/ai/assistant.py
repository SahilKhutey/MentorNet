from app.models.profile import Profile

def draft_connection_request(student_profile: Profile, mentor_profile: Profile) -> str:
    """
    AI-powered connection request drafter.
    Uses research interests to build a compelling outreach message.
    """
    field = mentor_profile.primary_field
    inst = mentor_profile.institution
    
    # Heuristic for high-conversion outreach
    draft = f"Hi {mentor_profile.full_name},\n\n"
    draft += f"I've been following your work at {inst} regarding {field}. "
    draft += f"As a student focusing on {student_profile.primary_field}, I believe your insights would be invaluable to my research journey.\n\n"
    draft += f"I'd love to connect and discuss potential mentorship. Best regards!"
    
    return draft

def summarize_mentor_profile(profile: Profile) -> str:
    """
    AI-generated summary of a mentor's key impact areas.
    """
    tags = ", ".join([t.name for t in profile.tags[:3]])
    summary = f"{profile.full_name} is an expert in {profile.primary_field} based at {profile.institution}. "
    if tags:
        summary += f"They specialize in {tags}. "
    summary += f"Their work is highly relevant for students interested in {profile.primary_field}."
    
    return summary
