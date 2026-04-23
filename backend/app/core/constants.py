from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    RESEARCHER = "researcher"

class MentorshipStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"

# Pagination constants
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
