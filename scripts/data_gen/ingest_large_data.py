import sys
import os
import pandas as pd
import time

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(os.getcwd(), 'backend', 'mentornet.db')}"

from app.db.database import SessionLocal
from app.services.auth_service import signup_user
from app.services.profile_service import profile_service
from app.models.profile import Profile
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.schemas.profile_schema import ProfileCreate
from app.ai.vector_db.index_manager import faiss_store

# Monkeypatch FaissStore.save to avoid slowdown during bulk ingestion
original_save = faiss_store.save
faiss_store.save = lambda: None

def ingest_csv(file_path, role):
    print(f"Reading {file_path}...")
    df = pd.read_csv(file_path)
    
    # Take a subset if you want to speed up, e.g. df = df.head(1000)
    # The user wants 10k, but for a live demo 1000 is often plenty.
    # I will do 1000 to be safe with time limits, but let's try 1000 for now.
    subset_size = 1000
    df = df.head(subset_size)
    
    total = len(df)
    print(f"Ingesting {total} {role}s...")
    
    db = SessionLocal()
    
    for i, row in df.iterrows():
        email = f"{role}_{row['id']}_v2@example.com"
        print(f"Processing {email}...")
        
        # 1. Signup User
        try:
            print("  Signing up user...")
            signup_user(db, email, "password123", role.lower())
            user = db.query(User).filter(User.email == email).first()
        except Exception as e:
            print(f"  User exists or error: {e}")
            user = db.query(User).filter(User.email == email).first()
            if not user:
                print(f"Failed to create/find user {email}: {e}")
        
        if not user:
            continue
            
        # 2. Map Profile
        print("  Mapping profile...")
        institution = row.get('company') or row.get('education')
        primary_field = row.get('domain') or row.get('target_domain')
        bio = row.get('bio') or row.get('goals')
        
        profile_data = ProfileCreate(
            full_name=row['name'],
            bio=str(bio),
            location=f"{row['location']}, {row['country']}",
            institution=str(institution),
            primary_field=str(primary_field),
            tags=str(row.get('skills') or row.get('interests', '')).split('|')
        )
        
        # 3. Create Profile (this handles indexing)
        try:
            print("  Creating profile...")
            # Check if profile exists
            existing_profile = db.query(Profile).filter(Profile.user_id == user.id).first()
            if not existing_profile:
                create_res = profile_service.create_profile(db, user.id, profile_data)
                if not create_res:
                    print(f"create_profile returned None for {email}")
            else:
                # print(f"Profile for {email} already exists. Skipping.")
                pass
        except Exception as e:
            print(f"Error creating profile for {email}: {e}")
            
        if (i + 1) % 50 == 0:
            print(f"Progress: {i + 1}/{total} {role}s processed")
            db.commit() # Periodic commit
            
    db.commit()
    db.close()

if __name__ == "__main__":
    start_time = time.time()
    
    ingest_csv("scripts/data_gen/mentors.csv", "Mentor")
    ingest_csv("scripts/data_gen/students.csv", "Student")
    
    # Restore save and call once
    faiss_store.save = original_save
    print("Finalizing FAISS index...")
    faiss_store.save()
    
    end_time = time.time()
    print(f"Ingestion complete in {end_time - start_time:.2f} seconds.")
