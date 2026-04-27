from app.db.database import SessionLocal
from app.models.badge import Badge
from app.models.user import User # Load User model to resolve relationship
from app.models.profile import Profile
from app.models.analytics import MentorAnalytics

def seed_badges():
    db = SessionLocal()
    
    badges = [
        {"name": "Elite Connector", "icon": "zap", "description": "Successfully completed 50+ mentorship sessions.", "rarity": "elite"},
        {"name": "Top Rated", "icon": "star", "description": "Maintained a 4.9+ average rating from students.", "rarity": "rare"},
        {"name": "Viral Mentor", "icon": "share", "description": "Brought in 10+ new users through referrals.", "rarity": "rare"},
        {"name": "Knowledge Pioneer", "icon": "book-open", "description": "Contributed highly-rated roadmaps to the community.", "rarity": "elite"}
    ]
    
    for b in badges:
        existing = db.query(Badge).filter(Badge.name == b["name"]).first()
        if not existing:
            db.add(Badge(**b))
    
    db.commit()
    print("Badges seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_badges()
