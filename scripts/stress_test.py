import sys
import os
import time
import random
import uuid
from faker import Faker
from sqlalchemy.orm import Session

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

# Import everything to ensure all models are registered in the same Base metadata
from app.db.database import SessionLocal
from app.models.user import User
from app.models.profile import Profile, Experience, Publication
from app.models.tag import Tag
from app.models.booking import Booking
from app.models.feedback import Feedback
from app.core.security import hash_password

fake = Faker()
NUM_TOTAL = 20000

def run_stress_test():
    print(f"Starting Stress Test: Generating {NUM_TOTAL} users...")
    db: Session = SessionLocal()
    
    # We must ensure all models are visible to the mapper configuration
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    
    start_time = time.time()

    users = []
    profiles = []

    domains = ["Software Engineering", "AI/ML", "Data Science", "Design", "Product"]
    roles = ["mentor", "student"]

    for i in range(NUM_TOTAL):
        role = random.choice(roles)
        user_id = str(uuid.uuid4())
        username = f"{fake.user_name()}_{i}"
        
        # Create User Object
        user = User(
            id=user_id,
            name=fake.name(),
            email=f"stress_{i}_{int(time.time())}@mentornet.ai",
            username=username,
            password="prehashed_password123", # Static string for speed in stress test
            role=role,
            referral_code=str(uuid.uuid4())[:8]
        )
        users.append(user)

        # Create Profile Object
        profile = Profile(
            user_id=user_id,
            bio=fake.paragraph(),
            location=f"{fake.city()}, India",
            institution=random.choice(["IIT Delhi", "Google", "Microsoft", "BITS Pilani"]),
            primary_field=random.choice(domains)
        )
        profiles.append(profile)

        if (i + 1) % 5000 == 0:
            print(f"Generated {i + 1} records...")

    print("Bulk saving to Database...")
    try:
        # Save in chunks to avoid memory issues
        chunk_size = 2000
        for i in range(0, len(users), chunk_size):
            db.bulk_save_objects(users[i:i+chunk_size])
            db.bulk_save_objects(profiles[i:i+chunk_size])
            db.commit()
            print(f"Committed chunk {i//chunk_size + 1}")
            
    except Exception as e:
        print(f"Error during bulk save: {e}")
        db.rollback()
    finally:
        db.close()

    end_time = time.time()
    print("Stress Test Injection Complete!")
    print(f"Total Records: {NUM_TOTAL}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    run_stress_test()
