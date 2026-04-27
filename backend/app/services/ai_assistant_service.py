from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.ai.embedding import generate_embedding
from app.ai.vector_db.index_manager import faiss_store
from app.models.profile import Profile
from app.models.user import User
from app.core.constants import UserRole
from app.services.llm_service import llm_service
from app.services.hybrid_search_service import hybrid_search

class AIAssistantService:
    def get_response(self, query: str, user_context: Dict[str, Any], db: Session) -> str:
        """
        Generates an AI response based on the research query, user context, and RAG retrieval.
        """
        # Step 1: Use Hybrid Search for personalized, ranked candidates
        user_id = user_context.get("user_id")
        ranked_results = hybrid_search(db, query, user_id=user_id, limit=5)
        
        # Step 2: Extract profiles (hybrid_search returns list of Profile objects or (Profile, score) tuples)
        # Assuming hybrid_search returns [(Profile, score), ...] as per its definition
        mentors = [p for p, score in ranked_results]
        
        # Step 4: Synthesize response via LLM service
        return llm_service.generate_response(query, user_context, mentors)

ai_assistant_service = AIAssistantService()
