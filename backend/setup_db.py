import sys
import os

# Add the current directory to sys.path to import from 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models import user, profile, mentor, student, tag, recommendation, session, feedback, availability, analytics

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
