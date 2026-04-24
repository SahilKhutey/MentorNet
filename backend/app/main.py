import os
from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.ai.vector_db.index_manager import faiss_store
from app.services.socket_manager import socket_app
from app.core.logging import setup_logging
from contextlib import asynccontextmanager
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize Sentry
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.2, # 20% tracing for production
    )

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load FAISS index
    print(f"FAISS index loaded: {len(faiss_store.id_map)} vectors")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Academic Networking Platform Backend",
    version=settings.VERSION,
    lifespan=lifespan
)

# Prometheus Instrumentation
Instrumentator().instrument(app).expose(app)

from app.core.security import rate_limit_middleware
from app.core.audit import audit_log_middleware

app.middleware("http")(rate_limit_middleware)
app.middleware("http")(audit_log_middleware)

# Configure Hardened CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True, # Required for secure cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

# Custom Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "active"
    }

# Health Check V2
@app.get("/health")
async def health():
    from app.db.database import SessionLocal
    from app.core.cache import cache_manager
    
    health_status = {"status": "healthy", "services": {}}
    
    # Check DB
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "up"
        db.close()
    except Exception:
        health_status["services"]["database"] = "down"
        health_status["status"] = "degraded"

    # Check Redis
    health_status["services"]["redis"] = "up" if cache_manager.enabled else "down"
    
    return health_status

# Include routers
from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount Socket.io
app.mount("/socket.io", socket_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
