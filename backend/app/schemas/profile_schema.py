from pydantic import BaseModel
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
    user_id: int
    
    class Config:
        from_attributes = True
