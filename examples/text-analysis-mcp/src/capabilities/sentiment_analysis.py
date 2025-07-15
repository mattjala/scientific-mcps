import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, Any
import json

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze the sentiment of the given text using NLTK's VADER sentiment analyzer.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dict containing sentiment scores and overall classification
    """
    if not text or not text.strip():
        return {
            "error": "Text cannot be empty",
            "content": [{"text": json.dumps({"error": "Text cannot be empty"})}],
            "_meta": {"tool": "sentiment_analysis", "error": "ValueError"},
            "isError": True
        }
    
    try:
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        
        # Determine overall sentiment
        if scores['compound'] >= 0.05:
            overall_sentiment = "positive"
        elif scores['compound'] <= -0.05:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "sentiment_scores": {
                "positive": scores['pos'],
                "negative": scores['neg'],
                "neutral": scores['neu'],
                "compound": scores['compound']
            },
            "overall_sentiment": overall_sentiment,
            "confidence": abs(scores['compound'])
        }
    except Exception as e:
        return {
            "error": str(e),
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "sentiment_analysis", "error": type(e).__name__},
            "isError": True
        }