import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag
from typing import Dict, Any, List
import json
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng')

def extract_keywords(text: str, num_keywords: int = 10) -> Dict[str, Any]:
    """
    Extract keywords from the given text using frequency analysis and POS tagging.
    
    Args:
        text: The text to extract keywords from
        num_keywords: Number of keywords to extract (default: 10)
        
    Returns:
        Dict containing keywords with their frequencies and metadata
    """
    if not text or not text.strip():
        return {
            "error": "Text cannot be empty",
            "content": [{"text": json.dumps({"error": "Text cannot be empty"})}],
            "_meta": {"tool": "keyword_extraction", "error": "ValueError"},
            "isError": True
        }
    
    try:
        # Tokenize and clean text
        tokens = word_tokenize(text.lower())
        
        # Remove punctuation and non-alphabetic tokens
        tokens = [token for token in tokens if token.isalpha()]
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        
        # Filter by minimum length
        tokens = [token for token in tokens if len(token) > 2]
        
        if not tokens:
            return {
                "error": "No valid tokens found after processing",
                "content": [{"text": json.dumps({"error": "No valid tokens found"})}],
                "_meta": {"tool": "keyword_extraction", "error": "ValueError"},
                "isError": True
            }
        
        # POS tagging to filter for nouns and adjectives
        pos_tags = pos_tag(tokens)
        relevant_tokens = [word for word, pos in pos_tags if pos.startswith('NN') or pos.startswith('JJ')]
        
        # Calculate frequency distribution
        freq_dist = FreqDist(relevant_tokens)
        
        # Get top keywords
        top_keywords = freq_dist.most_common(num_keywords)
        
        # Calculate additional metrics
        total_tokens = len(tokens)
        unique_tokens = len(set(tokens))
        
        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "keywords": [
                {
                    "word": word,
                    "frequency": count,
                    "relative_frequency": count / total_tokens
                }
                for word, count in top_keywords
            ],
            "total_tokens": total_tokens,
            "unique_tokens": unique_tokens,
            "vocabulary_diversity": unique_tokens / total_tokens if total_tokens > 0 else 0,
            "extracted_count": len(top_keywords)
        }
    except Exception as e:
        return {
            "error": str(e),
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "keyword_extraction", "error": type(e).__name__},
            "isError": True
        }