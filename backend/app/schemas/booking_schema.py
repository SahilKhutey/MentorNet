from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateBooking(BaseModel):
    mentor_id: str
    start_time: datetime
    end_time: datetime

class BookingResponse(BaseModel):
    id: str
    mentor_id: str
    student_id: str
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        from_attributes = True

class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime

class AvailabilityResponse(BaseModel):
    id: str
    mentor_id: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True
