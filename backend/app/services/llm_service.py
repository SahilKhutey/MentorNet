from typing import List, Dict, Any
import random

class LLMService:
    def generate_response(self, query: str, user_context: Dict[str, Any], retrieved_mentors: List[Any]) -> str:
        """
        Synthesizes a response using RAG context.
        """
        user_name = user_context.get("full_name", "Researcher")
        user_field = user_context.get("field", "Academic")
        
        # Construct the context string
        mentor_names = [m.full_name for m in retrieved_mentors[:3]]
        
        if not retrieved_mentors:
            return f"Hello {user_name}. I've analyzed your query regarding '{query}', but I couldn't find exact mentor matches in our current elite pool. However, based on your field in {user_field}, I recommend looking into interdisciplinary research nodes."

        # Elite Scholarly Prism Tone
        primary_mentor = retrieved_mentors[0]
        expertise = [t.name for t in primary_mentor.tags[:2]]
        
        response_templates = [
            f"Salutations, {user_name}. Analyzing the Scholarly Prism for '{query}'... I've identified a high-velocity alignment with {primary_mentor.full_name}. Their recognized expertise in {', '.join(expertise)} makes them an optimal match for your current research trajectory in {user_field}. Shall I initiate a connection or generate a research roadmap based on their previous collaborations?",
            f"Insight generated for '{query}', {user_name}. My semantic engine detects a significant overlap between your profile and the work of {primary_mentor.full_name} at their respective institution. Given your focus on {user_field}, their mentorship could accelerate your path toward high-impact publication. Would you like to review their availability?",
            f"The mentor network indicates a 98% match for your query regarding '{query}'. {primary_mentor.full_name} is currently leading research nodes that parallel your interests. Their influence in {expertise[0] if expertise else 'the field'} is substantial. I recommend a direct inquiry to discuss potential synergy. Shall I draft the communication?"
        ]
        
        return random.choice(response_templates)

llm_service = LLMService()
