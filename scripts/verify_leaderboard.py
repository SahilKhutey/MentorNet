import sys
import os
# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))
from app.db.database import SessionLocal
from app.models.user import User
from app.models.profile import Profile
from app.models.tag import Tag
from sqlalchemy.orm import configure_mappers
configure_mappers()

from app.services.ranking_service import get_trending_mentors

def verify_leaderboard():
    print("Fetching Top Mentors from the 20,000 user dataset...")
    db = SessionLocal()
    
    try:
        top_mentors = get_trending_mentors(db, limit=10)
        
        print("\n--- MENTORNET GLOBAL LEADERBOARD ---")
        print("-" * 40)
        for i, mentor in enumerate(top_mentors):
            print(f"{i+1}. {mentor['name']} (@{mentor['username']})")
            print(f"   Score: {mentor['score']} | Badges: {', '.join(mentor['badges']) if mentor['badges'] else 'None'}")
            print("-" * 40)
            
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_leaderboard()
