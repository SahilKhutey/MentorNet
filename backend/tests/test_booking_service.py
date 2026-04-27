import pytest
from sqlalchemy import create_session
from sqlalchemy.orm import Session
from app.services.booking_service import booking_service
from app.models.availability import Availability
from app.models.booking import Booking
from datetime import datetime, timedelta
import uuid

# Mock DB session for testing
@pytest.fixture
def db_session():
    # In a real app, use a test DB. For now, we mock the logic.
    pass

def test_create_booking_success(mocker):
    db = mocker.Mock(spec=Session)
    
    # Mock Availability
    slot_id = str(uuid.uuid4())
    mentor_id = "mentor_123"
    student_id = "student_456"
    mock_slot = Availability(
        id=slot_id,
        mentor_id=mentor_id,
        start_time=datetime.utcnow() + timedelta(days=1),
        end_time=datetime.utcnow() + timedelta(days=1, minutes=30)
    )
    
    # Mock query behavior
    mocker.patch.object(db.query(Availability), 'filter', return_value=db.query(Availability))
    mocker.patch.object(db.query(Availability).filter(), 'first', return_value=mock_slot)
    
    # Run service
    booking = booking_service.create_booking(
        db, 
        student_id=student_id, 
        mentor_id=mentor_id, 
        slot_id=slot_id, 
        topic="Career Growth", 
        notes="Testing"
    )
    
    assert booking.student_id == student_id
    assert booking.mentor_id == mentor_id
    assert booking.topic == "Career Growth"
    db.add.assert_called()
    db.delete.assert_called_with(mock_slot)
    db.commit.assert_called()

def test_create_booking_failure_no_slot(mocker):
    db = mocker.Mock(spec=Session)
    
    # Mock query to return None
    mocker.patch.object(db.query(Availability), 'filter', return_value=db.query(Availability))
    mocker.patch.object(db.query(Availability).filter(), 'first', return_value=None)
    
    with pytest.raises(Exception) as excinfo:
        booking_service.create_booking(
            db, 
            student_id="student_456", 
            mentor_id="mentor_123", 
            slot_id="invalid_slot", 
            topic="Career Growth", 
            notes="Testing"
        )
    
    assert "Availability slot not found" in str(excinfo.value)
