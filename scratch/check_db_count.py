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

db = SessionLocal()
count = db.query(User).count()
print(f"Current User Count: {count}")
db.close()
