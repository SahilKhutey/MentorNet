from fastapi import APIRouter, Depends
import psutil
import os
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.config import settings
from app.core.cache import cache_manager
import time

router = APIRouter(prefix="/ops", tags=["Operations"])

@router.get("/health")
def system_health(db: Session = Depends(get_db)):
    """
    Comprehensive system health check for production monitoring.
    """
    health = {
        "status": "online",
        "timestamp": time.time(),
        "services": {},
        "resources": {}
    }

    # 1. Database Check
    try:
        db.execute("SELECT 1")
        health["services"]["database"] = "healthy"
    except Exception as e:
        health["services"]["database"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"

    # 2. Redis Check
    if cache_manager.enabled:
        try:
            cache_manager.redis.ping()
            health["services"]["redis"] = "healthy"
        except Exception:
            health["services"]["redis"] = "unhealthy"
            health["status"] = "degraded"
    else:
        health["services"]["redis"] = "disabled"

    # 3. Vector DB (FAISS) Check
    index_path = settings.FAISS_INDEX_PATH
    if os.path.exists(index_path):
        health["services"]["faiss"] = {
            "status": "healthy",
            "index_size_mb": round(os.path.getsize(index_path) / (1024 * 1024), 2)
        }
    else:
        health["services"]["faiss"] = "missing"

    # 4. OS Resource Check
    health["resources"] = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

    return health
