import os
import sys
import json
from fastmcp import FastMCP
from dotenv import load_dotenv

# Ensure parent directory is on PYTHONPATH so "capabilities" can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load .env variables, if any
load_dotenv()

# Import our text analysis handlers
import mcp_handlers

# Initialize FastMCP server
mcp = FastMCP("TextAnalysisMCP")

# ─── SENTIMENT ANALYSIS TOOL ─────────────────────────────────────────────────────────
@mcp.tool(
    name="analyze_sentiment",
    description="Analyze the sentiment of text using NLTK's VADER sentiment analyzer. Returns positive, negative, neutral, and compound scores along with overall sentiment classification."
)
async def analyze_sentiment_tool(text: str) -> dict:
    """Analyze sentiment of the given text."""
    try:
        return await mcp_handlers.analyze_sentiment_handler(text)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "analyze_sentiment", "error": type(e).__name__},
            "isError": True
        }


# ─── KEYWORD EXTRACTION TOOL ─────────────────────────────────────────────────────────
@mcp.tool(
    name="extract_keywords",
    description="Extract keywords from text using frequency analysis and part-of-speech tagging. Focuses on nouns and adjectives for better keyword quality."
)
async def extract_keywords_tool(text: str, num_keywords: int = 10) -> dict:
    """Extract keywords from the given text."""
    try:
        return await mcp_handlers.extract_keywords_handler(text, num_keywords)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "extract_keywords", "error": type(e).__name__},
            "isError": True
        }

# ─── READABILITY ANALYSIS TOOL ─────────────────────────────────────────────────────────
@mcp.tool(
    name="analyze_readability",
    description="Analyze the readability of text using various metrics including Flesch Reading Ease, Flesch-Kincaid Grade Level, Coleman-Liau Index, and Automated Readability Index."
)
async def analyze_readability_tool(text: str) -> dict:
    """Analyze readability of the given text."""
    try:
        return await mcp_handlers.analyze_readability_handler(text)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "analyze_readability", "error": type(e).__name__},
            "isError": True
        }

def main():
    """
    Main entry point to run the Text Analysis MCP server.
    Chooses between stdio or SSE transport based on MCP_TRANSPORT.
    """
    try:
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport == "sse":
            host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = int(os.getenv("MCP_SSE_PORT", "8000"))
            print(json.dumps({"message": f"Starting SSE on {host}:{port}"}), file=sys.stderr)
            mcp.run(transport="sse", host=host, port=port)
        else:
            mcp.run(transport="stdio")
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()