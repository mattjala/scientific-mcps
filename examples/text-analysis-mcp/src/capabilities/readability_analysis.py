import textstat
from typing import Dict, Any
import json

def analyze_readability(text: str) -> Dict[str, Any]:
    """
    Analyze the readability of the given text using various metrics.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dict containing readability scores and metrics
    """
    if not text or not text.strip():
        return {
            "error": "Text cannot be empty",
            "content": [{"text": json.dumps({"error": "Text cannot be empty"})}],
            "_meta": {"tool": "readability_analysis", "error": "ValueError"},
            "isError": True
        }
    
    try:
        # Calculate various readability metrics
        flesch_score = textstat.flesch_reading_ease(text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        coleman_liau_index = textstat.coleman_liau_index(text)
        automated_readability_index = textstat.automated_readability_index(text)
        
        # Basic text statistics
        sentence_count = textstat.sentence_count(text)
        word_count = textstat.lexicon_count(text)
        char_count = textstat.char_count(text)
        syllable_count = textstat.syllable_count(text)
        
        # Interpret Flesch Reading Ease score
        if flesch_score >= 90:
            reading_level = "Very Easy"
        elif flesch_score >= 80:
            reading_level = "Easy"
        elif flesch_score >= 70:
            reading_level = "Fairly Easy"
        elif flesch_score >= 60:
            reading_level = "Standard"
        elif flesch_score >= 50:
            reading_level = "Fairly Difficult"
        elif flesch_score >= 30:
            reading_level = "Difficult"
        else:
            reading_level = "Very Difficult"
        
        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "readability_scores": {
                "flesch_reading_ease": flesch_score,
                "flesch_kincaid_grade": flesch_kincaid_grade,
                "coleman_liau_index": coleman_liau_index,
                "automated_readability_index": automated_readability_index
            },
            "reading_level": reading_level,
            "text_statistics": {
                "sentence_count": sentence_count,
                "word_count": word_count,
                "character_count": char_count,
                "syllable_count": syllable_count,
                "avg_words_per_sentence": word_count / sentence_count if sentence_count > 0 else 0,
                "avg_syllables_per_word": syllable_count / word_count if word_count > 0 else 0
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "readability_analysis", "error": type(e).__name__},
            "isError": True
        }