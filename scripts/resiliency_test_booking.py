import threading
import time
import sys
import os
from sqlalchemy.orm import Session

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.db.database import SessionLocal
from app.models.availability import Availability
from app.services.booking_service import booking_service

def attempt_booking(thread_id, results, student_id, mentor_id, slot_id):
    db = SessionLocal()
    try:
        print(f"Thread {thread_id}: Attempting to book slot {slot_id}...")
        booking = booking_service.create_booking(
            db, 
            student_id=student_id, 
            mentor_id=mentor_id, 
            slot_id=slot_id, 
            topic="Resiliency Test", 
            notes="Testing for race conditions"
        )
        results.append(f"Thread {thread_id}: SUCCESS")
    except Exception as e:
        results.append(f"Thread {thread_id}: FAILED - {str(e)}")
    finally:
        db.close()

def run_resiliency_test():
    db = SessionLocal()
    
    # 1. Setup: Create a single availability slot for the future
    mentor_id = "mentor-123"
    student_prefix = "student-"
    
    # Clean up existing
    db.query(Availability).filter(Availability.mentor_id == mentor_id).delete()
    db.commit()
    
    from datetime import datetime, timedelta
    slot = Availability(
        id="test-slot-uuid",
        mentor_id=mentor_id,
        start_time=datetime.now() + timedelta(hours=1),
        end_time=datetime.now() + timedelta(hours=2)
    )
    db.add(slot)
    db.commit()
    
    print(f"--- Starting Resiliency Test (Race Condition Check) ---")
    print(f"Initial Slot: {slot.id} for Mentor: {mentor_id}")
    
    # 2. Spawn 10 concurrent threads to book the SAME slot
    threads = []
    results = []
    num_threads = 10
    
    for i in range(num_threads):
        t = threading.Thread(
            target=attempt_booking, 
            args=(i, results, f"{student_prefix}{i}", mentor_id, slot.id)
        )
        threads.append(t)
    
    # Start all threads simultaneously
    for t in threads:
        t.start()
    
    # Wait for all to finish
    for t in threads:
        t.join()
        
    # 3. Analyze Results
    success_count = len([r for r in results if "SUCCESS" in r])
    fail_count = len([r for r in results if "FAILED" in r])
    
    print("\n--- Test Results ---")
    for r in results:
        print(r)
        
    print(f"\nSummary:")
    print(f"Total Attempts: {num_threads}")
    print(f"Successful Bookings: {success_count}")
    print(f"Failed Bookings: {fail_count}")
    
    if success_count == 1:
        print("\nPASS: Only one booking succeeded. Race condition protection is active.")
    else:
        print(f"\nFAIL: {success_count} bookings succeeded! Race condition detected.")

if __name__ == "__main__":
    run_resiliency_test()
