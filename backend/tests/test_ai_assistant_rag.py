import sys
import os
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ai_assistant_service import ai_assistant_service
from app.models.profile import Profile
from app.core.constants import UserRole

def test_ai_assistant_rag_flow():
    # Mock DB session
    db = MagicMock()
    
    # Mock retrieved profiles
    mock_mentor = Profile(id=1, full_name="Dr. Jane Smith", primary_field="AI Research", bio="Elite researcher in AI.")
    
    # Mock the query results
    db.query.return_value.join.return_value.filter.return_value.all.return_value = [mock_mentor]
    
    context = {
        "full_name": "Test User",
        "field": "Computer Science"
    }
    
    query = "Who is the best mentor for AI?"
    
    print(f"Testing query: {query}")
    response = ai_assistant_service.get_response(query, context, db)
    
    print(f"Response: {response}")
    assert "Jane Smith" in response
    assert "AI Research" in response or "Computer Science" in response
    print("Test passed!")

if __name__ == "__main__":
    test_ai_assistant_rag_flow()
