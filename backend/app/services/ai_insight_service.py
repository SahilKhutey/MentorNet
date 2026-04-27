from sqlalchemy.orm import Session
from app.models.session import Session as MentorshipSession
from typing import List, Dict
import random

class AIInsightService:
    @staticmethod
    def generate_session_summary(transcript: str) -> Dict:
        """
        Simulates an AI extraction of key insights from a session transcript.
        In production, this would call Gemini or another LLM.
        """
        # Mock insights based on potential transcript keywords
        insights_pool = [
            "Use Redis for caching high-frequency leaderboard queries.",
            "Always unify your database Base classes to avoid circular dependencies.",
            "Vertical scaling is a temporary fix; horizontal is the production standard.",
            "Implement rate limiting on public endpoints to prevent scraping.",
            "Use vector embeddings for semantic search instead of keyword matching.",
            "Optimize database indexes for read-heavy workloads.",
            "Consider event-driven architecture for background tasks.",
            "Prioritize UX micro-animations to increase user retention."
        ]
        
        # Select 3 random insights
        extracted_insights = random.sample(insights_pool, 3)
        
        summary = f"A productive deep-dive into system architecture and optimization strategies. Focused on scaling from 10k to 100k users."
        
        return {
            "summary": summary,
            "insights": extracted_insights
        }

    @staticmethod
    def update_session_insights(db: Session, session_id: str, transcript: str):
        session = db.query(MentorshipSession).filter(MentorshipSession.id == session_id).first()
        if not session:
            return None
        
        ai_data = AIInsightService.generate_session_summary(transcript)
        session.ai_summary = ai_data["summary"]
        session.ai_insights = ai_data["insights"]
        
        db.commit()
        db.refresh(session)
        return session

ai_insight_service = AIInsightService()
