from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
import re

class SignupRequest(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    password: constr(min_length=8)
    role: constr(pattern="^(mentor|student)$")
    referral_code: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_must_be_alphanumeric_space(cls, v):
        if not re.match(r"^[a-zA-Z\s]+$", v):
            raise ValueError('Name must contain only letters and spaces')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
