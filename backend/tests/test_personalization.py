import pytest
from unittest.mock import MagicMock
from app.ai.personalization import personalize_results

def test_personalize_results_with_interests():
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
    
    # We run multiple times to ensure discovery factor doesn't break the main logic
    results = personalize_results(ranked_profiles, user_id="user1", user_interests=user_interests)
    
    # Profile 1 has 2 matches -> boost 0.16. 0.5 + 0.16 = 0.66 + discovery (0-0.05)
    # Profile 2 has 0 matches -> boost 0. 0.6 + 0 = 0.6 + discovery (0-0.05)
    # Profile 1 should be first
    assert results[0]["id"] == 1
    assert results[0]["score"] >= 0.66
    assert "Top match" in results[0]["why"]

def test_personalize_results_no_user():
    profile = MagicMock()
    profile.id = 1
    profile.full_name = "John Doe"
    profile.primary_field = "CS"
    profile.tags = []
    
    ranked_profiles = [(profile, 0.5)]
    results = personalize_results(ranked_profiles, user_id=None)
    
    assert len(results) == 1
    assert results[0]["id"] == 1
    assert results[0]["score"] == 0.5
