import json
from typing import Any, Dict, Optional
from capabilities import sentiment_analysis, keyword_extraction, readability_analysis

class UnknownToolError(Exception):
    """Raised when an unsupported tool_name is requested."""
    pass

async def analyze_sentiment_handler(text: str) -> Dict[str, Any]:
    """
    Handler for sentiment analysis tool.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dict containing sentiment analysis results
    """
    try:
        return sentiment_analysis.analyze_sentiment(text)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "analyze_sentiment", "error": type(e).__name__},
            "isError": True
        }


async def extract_keywords_handler(text: str, num_keywords: int = 10) -> Dict[str, Any]:
    """
    Handler for keyword extraction tool.
    
    Args:
        text: The text to extract keywords from
        num_keywords: Number of keywords to extract
        
    Returns:
        Dict containing keyword extraction results
    """
    try:
        return keyword_extraction.extract_keywords(text, num_keywords)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "extract_keywords", "error": type(e).__name__},
            "isError": True
        }

async def analyze_readability_handler(text: str) -> Dict[str, Any]:
    """
    Handler for readability analysis tool.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dict containing readability analysis results
    """
    try:
        return readability_analysis.analyze_readability(text)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "analyze_readability", "error": type(e).__name__},
            "isError": True
        }