from fastapi import APIRouter
from app.api.v1.endpoints import (
    profile, auth, search, recommendation, 
    feedback, analytics, booking, session, chat, ops, ai_assistant, enterprise,
    user, roadmap, resume, kb
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(profile.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(search.router)
api_router.include_router(recommendation.router)
api_router.include_router(feedback.router)
api_router.include_router(analytics.router)
api_router.include_router(booking.router)
api_router.include_router(session.router)
api_router.include_router(chat.router)
api_router.include_router(ops.router)
api_router.include_router(ai_assistant.router)
api_router.include_router(enterprise.router)
api_router.include_router(roadmap.router)
api_router.include_router(resume.router)
api_router.include_router(kb.router)
