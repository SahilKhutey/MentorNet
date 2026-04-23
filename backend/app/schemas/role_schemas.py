from pydantic import BaseModel

class MentorCreate(BaseModel):
    designation: str
    organization: str
    experience_years: int
    availability: str

class StudentCreate(BaseModel):
    degree: str
    year_of_study: int
    goals: str
