from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.ai.vector_db.index_manager import faiss_store
from app.services.socket_manager import socket_app
from app.core.logging import setup_logging

setup_logging()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load FAISS index
    print(f"FAISS index loaded: {len(faiss_store.id_map)} vectors")
    yield
    # Shutdown logic can go here

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Academic Networking Platform Backend",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

from app.core.security import rate_limit_middleware

app.middleware("http")(rate_limit_middleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "active"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

# Include routers
from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount Socket.io
app.mount("/socket.io", socket_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
