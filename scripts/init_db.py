import sys
import os
# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.db.database import engine
from app.db.base_class import Base

# Import all models to ensure they are registered on the Base.metadata
import app.models

def init_db():
    print("Dropping all existing tables for a clean sync...")
    Base.metadata.drop_all(bind=engine)
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()
