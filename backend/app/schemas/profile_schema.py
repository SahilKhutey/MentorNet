from pydantic import BaseModel, model_validator
from typing import List, Optional

class ProfileBase(BaseModel):
    full_name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    institution: Optional[str] = None
    primary_field: Optional[str] = None

class ProfileCreate(ProfileBase):
    tags: List[str]

class ProfileUpdate(ProfileBase):
    tags: Optional[List[str]] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: str
    username: Optional[str] = None
    referral_code: Optional[str] = None
    tags: List[str] = []

    @model_validator(mode='before')
    @classmethod
    def from_orm(cls, obj):
        # Handle case where obj is already a dict (e.g. from tests)
        if isinstance(obj, dict):
            return obj
        
        # Extract data from SQLAlchemy object
        return {
            "id": obj.id,
            "user_id": obj.user_id,
            "full_name": obj.full_name,
            "bio": obj.bio,
            "location": obj.location,
            "institution": obj.institution,
            "primary_field": obj.primary_field,
            "username": obj.user.username if obj.user else None,
            "referral_code": obj.user.referral_code if obj.user else None,
            "tags": [t.name for t in obj.tags] if hasattr(obj, 'tags') else []
        }

    class Config:
        from_attributes = True
