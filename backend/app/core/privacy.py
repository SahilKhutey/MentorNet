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
