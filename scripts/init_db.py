import sys
import os
# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.db.database import engine
from app.db.base_class import Base

# Import all models to ensure they are registered on the Base.metadata
from app.models.user import User
from app.models.profile import Profile, Experience, Publication
from app.models.tag import Tag
from app.models.booking import Booking
from app.models.feedback import Feedback
from app.models.session import Session

def init_db():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()
