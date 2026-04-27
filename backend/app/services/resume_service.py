from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.services.ai_insight_service import ai_insight_service
import random

class ResumeService:
    @staticmethod
    def analyze_resume(db: Session, user_id: str, file_path: str):
        """
        Mock AI resume analysis logic.
        In production, this would use Gemini/OpenAI to parse the PDF.
        """
        # Create record
        resume = Resume(
            user_id=user_id,
            file_path=file_path
        )
        db.add(resume)
        
        # Mock analysis results
        analysis = {
            "strengths": [
                "Strong technical foundation in Python and Distributed Systems.",
                "Evidence of collaborative research in high-impact labs.",
                "Clear career progression towards Research Engineering."
            ],
            "weaknesses": [
                "Lack of specific quantified achievements in recent roles.",
                "Formatting could be optimized for ATS systems.",
                "Skills section is a bit cluttered."
            ],
            "mentor_recommendation": "We recommend connecting with Rahul Sharma for advice on distributed systems specialization.",
            "score": random.randint(70, 95)
        }
        
        resume.analysis_results = analysis
        resume.score = analysis["score"]
        
        db.commit()
        db.refresh(resume)
        return resume

resume_service = ResumeService()
