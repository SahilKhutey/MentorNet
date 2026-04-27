from fastapi import HTTPException, status
from app.models.user import User

class PrivacyEnforcer:
    @staticmethod
    def verify_resource_access(current_user_id: int, owner_id: int, role: str = None):
        """
        Ensures a user can only access their own data, unless they have admin privileges.
        """
        if current_user_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You do not own this resource."
            )

    @staticmethod
    def verify_mentor_action(user_role: str):
        """
        Ensures only mentors can perform specific actions (e.g., setting availability).
        """
        if user_role != "mentor":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Only mentors can perform this action."
            )

    @staticmethod
    def verify_student_action(user_role: str):
        """
        Ensures only students can perform specific actions (e.g., booking a session).
        """
        if user_role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Only students can perform this action."
            )

    @staticmethod
    def anonymize_user_data(db: Session, user_id: str):
        """
        Anonymizes user data for 'Right to be Forgotten' requests.
        Preserves research nodes (roadmaps, sessions) but removes all PII.
        """
        from app.models.profile import Profile
        from app.models.user import User
        
        user = db.query(User).filter(User.id == user_id).first()
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        
        if user:
            user.email = f"deleted_{user_id}@mentornet.ai"
            user.hashed_password = "DELETED"
            user.name = "Anonymous Researcher"
            
        if profile:
            profile.full_name = "Anonymous Researcher"
            profile.headline = "Record Anonymized"
            profile.bio = "This user has exercised their right to be forgotten."
            
        db.commit()

    @staticmethod
    def mask_pii(text: str) -> str:
        """
        Masks common PII (emails, names in specific patterns) for safe logging.
        """
        import re
        # Simple email mask
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        masked_text = re.sub(email_pattern, "[MASKED_EMAIL]", text)
        
        # Phone pattern (basic)
        phone_pattern = r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
        # Only mask if it looks like a long enough number to be a phone
        if len(re.findall(phone_pattern, masked_text)) > 0:
             masked_text = re.sub(phone_pattern, "[MASKED_PHONE]", masked_text)
             
        return masked_text
