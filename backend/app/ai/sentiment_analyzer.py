import re

def analyze_sentiment(text: str) -> float:
    """
    Analyzes the sentiment of a review text.
    Returns a score between -1.0 (very negative) and 1.0 (very positive).
    """
    if not text:
        return 0.0
        
    # Heuristic-based sentiment analysis as a production-grade fallback
    positive_words = {
        'excellent', 'great', 'awesome', 'helpful', 'insightful', 'amazing', 
        'fantastic', 'learned', 'highly', 'recommend', 'perfect', 'clear'
    }
    negative_words = {
        'poor', 'bad', 'waste', 'useless', 'confusing', 'late', 'rude', 
        'unhelpful', 'unclear', 'difficult', 'slow', 'bore'
    }
    
    text = text.lower()
    words = re.findall(r'\w+', text)
    
    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    
    total = pos_count + neg_count
    if total == 0:
        return 0.0
        
    return (pos_count - neg_count) / total
