def build_profile_text(profile):
    tags = " ".join([t.name for t in profile.tags])

    text = f"""
    {profile.full_name}
    {profile.bio or ''}
    Field: {profile.primary_field or ''}
    Institution: {profile.institution or ''}
    Skills: {tags}
    """

    return text.strip()
