import sys
import os
sys.path.append("backend")
from app.core.config import settings
print(f"CORS Origins: {settings.BACKEND_CORS_ORIGINS}")
print(f"Type: {type(settings.BACKEND_CORS_ORIGINS)}")
