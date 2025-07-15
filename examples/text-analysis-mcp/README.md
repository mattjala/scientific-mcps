# Text Analysis MCP

A Model Context Protocol (MCP) server that provides text analysis capabilities using Python's NLTK library.

## Features

- **Sentiment Analysis**: Analyze text sentiment using NLTK's VADER sentiment analyzer
- **Keyword Extraction**: Extract important keywords using frequency analysis and POS tagging
- **Readability Analysis**: Analyze text readability using various metrics

## Installation

```bash
cd text-analysis-mcp
pip install -e .
```

## Usage

Run the MCP server:

```bash
text-analysis-mcp
```

## Demo

Run the demo script to see all tools in action:

```bash
python demo.py
```

The demo script will:
1. Start the MCP server
2. Initialize the MCP connection
3. List available tools
4. Test each tool with sample text
5. Display the results
6. Stop the server

## Tools

### analyze_sentiment
Analyze the sentiment of text using NLTK's VADER sentiment analyzer.

### extract_keywords
Extract keywords from text using frequency analysis and part-of-speech tagging.

### analyze_readability
Analyze the readability of text using various metrics including Flesch Reading Ease and Flesch-Kincaid Grade Level.

## Dependencies

- NLTK for natural language processing
- textstat for readability metrics
- FastMCP for MCP server implementation