#!/bin/bash
# Simple test runner for AI agent prompt tests
# Currently uses Claude Code CLI but designed to be agent-agnostic

set -e

# Check if we have the required dependencies
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not installed"
    exit 1
fi

# Check if AI agent CLI is available (currently Claude Code CLI)
if ! command -v claude &> /dev/null; then
    echo "Error: claude command is required but not found"
    echo "Please install Claude Code CLI first"
    exit 1
fi

# Install required packages if needed
echo "Installing required packages..."
pip install -q pyyaml jsonschema

# Run the tests
echo "Running AI agent prompt tests..."
python3 run_ai_tests.py