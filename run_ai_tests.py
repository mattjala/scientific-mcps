#!/usr/bin/env python3
"""
Main script to run AI agent prompt tests.
Currently uses Claude Code CLI but designed to be agent-agnostic.
"""
import sys
import argparse
from pathlib import Path
from ai_test_loader import AIAgentTestLoader


def main():
    """Main entry point for running tests."""
    parser = argparse.ArgumentParser(description='Run AI agent prompt tests')
    parser.add_argument(
        '--yaml',
        default='ai_agent_tests.yaml',
        help='Path to YAML test file (default: ai_agent_tests.yaml)'
    )
    
    args = parser.parse_args()
    
    # Check if test file exists
    if not Path(args.yaml).exists():
        print(f"Error: Test file '{args.yaml}' not found")
        sys.exit(1)
    
    try:
        # Initialize test loader
        loader = AIAgentTestLoader(args.yaml)
        
        print(f"Running tests from: {args.yaml}")
        print(f"Found {len(loader.tests)} test(s)")
        
        # Run all tests
        results = loader.run_all_tests()
        
        # Print results
        all_passed = loader.print_results(results)
        
        # Exit with appropriate code
        sys.exit(0 if all_passed else 1)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()