from fastapi import APIRouter
from app.api.v1.endpoints import (
    profile, auth, search, recommendation, 
    feedback, analytics, scheduling, chat, ops, ai_assistant, enterprise
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(profile.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(search.router)
api_router.include_router(recommendation.router)
api_router.include_router(feedback.router)
api_router.include_router(analytics.router)
api_router.include_router(scheduling.router)
api_router.include_router(chat.router)
api_router.include_router(ops.router)
api_router.include_router(ai_assistant.router)
api_router.include_router(enterprise.router)
