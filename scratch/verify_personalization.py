import sys
import os
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.ai.personalization import personalize_results

def run_test():
    # Mock profiles
    mock_tag1 = MagicMock()
    mock_tag1.name = "Python"
    
    mock_tag2 = MagicMock()
    mock_tag2.name = "AI"
    
    profile1 = MagicMock()
    profile1.id = 1
    profile1.full_name = "John Doe"
    profile1.primary_field = "Computer Science"
    profile1.tags = [mock_tag1, mock_tag2]
    
    profile2 = MagicMock()
    profile2.id = 2
    profile2.full_name = "Jane Smith"
    profile2.primary_field = "Physics"
    profile2.tags = []
    
    ranked_profiles = [(profile1, 0.5), (profile2, 0.6)]
    user_interests = ["Python", "AI"]
    
    results = personalize_results(ranked_profiles, user_id="user1", user_interests=user_interests)
    
    print(f"Result 1: {results[0]['name']} (Score: {results[0]['score']})")
    print(f"Result 2: {results[1]['name']} (Score: {results[1]['score']})")
    print(f"Reason: {results[0]['why']}")

    if results[0]["id"] == 1:
        print("TEST PASSED")
    else:
        print("TEST FAILED")

if __name__ == "__main__":
    run_test()
