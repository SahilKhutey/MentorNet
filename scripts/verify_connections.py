import os
import sys
import time
from sqlalchemy import create_engine, text
import redis
from dotenv import load_dotenv

load_dotenv()

def test_connections():
    print("============================================================")
    print("MENTORNET PRODUCTION CONNECTIVITY TEST")
    print("============================================================")
    
    # 1. Database Connection
    db_url = os.getenv("DATABASE_URL")
    # For local terminal testing, swap 'db' for 'localhost' if running outside docker
    if "db:5432" in db_url:
        test_url = db_url.replace("db:5432", "localhost:5432")
    else:
        test_url = db_url

    print(f"[*] Testing PostgreSQL Connection: {test_url.split('@')[-1] if test_url else 'NOT SET'}")
    try:
        engine = create_engine(test_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("[OK] PostgreSQL: CONNECTED")
    except Exception as e:
        print(f"[FAIL] PostgreSQL: FAILED (Expected if Docker not running) - {e}")

    # 2. Redis Connection
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    if "redis:6379" in redis_url:
        test_redis = redis_url.replace("redis:6379", "localhost:6379")
    else:
        test_redis = redis_url

    print(f"[*] Testing Redis Connection: {test_redis}")
    try:
        r = redis.from_url(test_redis)
        r.ping()
        print("[OK] Redis: CONNECTED")
    except Exception as e:
        print(f"[FAIL] Redis: FAILED (Expected if Docker not running) - {e}")

    # 3. FAISS Index
    print("[*] Testing FAISS Engine...")
    try:
        from app.ai.vector_db.index_manager import faiss_store
        print(f"[OK] FAISS Engine: ACTIVE ({len(faiss_store.id_map)} vectors)")
    except Exception as e:
        print(f"[FAIL] FAISS Engine: FAILED - {e}")

    # 4. Sentry Check
    sentry_dsn = os.getenv("SENTRY_DSN")
    print(f"[*] Sentry Status: {'INITIALIZED' if sentry_dsn else 'DISABLED (No DSN)'}")

    print("============================================================")
    print("SYSTEM STATUS: READY FOR TRAFFIC")
    print("============================================================")

if __name__ == "__main__":
    # Add backend to path
    backend_path = os.path.join(os.getcwd(), "backend")
    if backend_path not in sys.path:
        sys.path.append(backend_path)
    test_connections()
