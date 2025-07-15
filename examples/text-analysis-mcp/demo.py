#!/usr/bin/env python3
"""
Demo script for the Text Analysis MCP server.

This script demonstrates how to:
1. Start the MCP server as a subprocess
2. Send JSON-RPC requests to the server
3. Receive and parse responses
4. Terminate the server cleanly
"""

import json
import subprocess
import time
import sys
import os

# Sample text for testing all tools
SAMPLE_TEXT = "I love using Python for natural language processing! It's amazing how powerful NLTK is. However, sometimes the documentation can be confusing for beginners. Overall, I think Python is the best language for NLP tasks."

class MCPDemo:
    def __init__(self):
        self.server_process = None
        self._request_counter = 0
        
    def start_server(self):
        """Start the MCP server as a subprocess."""
        print("Starting Text Analysis MCP server...")
        
        # Start the server process
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Give the server a moment to start
        time.sleep(2)
        
        if self.server_process.poll() is not None:
            stderr_output = self.server_process.stderr.read()
            print(f"Server failed to start. Error: {stderr_output}")
            return False
            
        print("Server started successfully!")
        return True
    
    def send_request(self, method, params=None):
        """Send a JSON-RPC request to the server."""
        self._request_counter += 1
        request_id = self._request_counter
        
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        
        if params:
            request["params"] = params
            
        request_json = json.dumps(request) + "\n"
        
        print(f"Sending request: {method}")
        print(f"   Request data: {request_json.strip()}")
        
        # Send the request
        self.server_process.stdin.write(request_json)
        self.server_process.stdin.flush()
        
        # Read the response
        try:
            response_line = self.server_process.stdout.readline()
            if response_line:
                response = json.loads(response_line.strip())
                print(f"Received response:")
                print(json.dumps(response, indent=2))
                return response
            else:
                print("No response received")
                return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse response: {e}")
            print(f"   Raw response: {response_line}")
            return None
    
    def initialize_server(self):
        """Initialize the MCP server with required handshake."""
        print("\nInitializing MCP server...")
        
        # Send initialize request
        init_response = self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "text-analysis-demo",
                "version": "1.0.0"
            }
        })
        
        if init_response and "error" not in init_response:
            print("Server initialized successfully!")
            
            # Send initialized notification
            notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            notification_json = json.dumps(notification) + "\n"
            self.server_process.stdin.write(notification_json)
            self.server_process.stdin.flush()
            
            return True
        else:
            print("Failed to initialize server")
            return False
    
    def demo_tools(self):
        """Demonstrate the available tools."""
        print("\nGetting list of available tools...")
        
        # List available tools
        tools_response = self.send_request("tools/list")
        
        if tools_response and "result" in tools_response:
            tools = tools_response["result"]["tools"]
            print(f"Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description']}")
        
        print("\nTesting each tool with sample data...")
        
        # Test sentiment analysis
        print("\n1. Testing sentiment analysis...")
        sentiment_response = self.send_request("tools/call", {
            "name": "analyze_sentiment",
            "arguments": {
                "text": SAMPLE_TEXT
            }
        })
        
        if sentiment_response and "result" in sentiment_response:
            result = sentiment_response["result"]["content"][0]["text"]
            data = json.loads(result)
            print(f"   Sentiment: {data.get('overall_sentiment', 'unknown')}")
            print(f"   Confidence: {data.get('confidence', 0):.2f}")
        
        # Test keyword extraction
        print("\n2. Testing keyword extraction...")
        keywords_response = self.send_request("tools/call", {
            "name": "extract_keywords",
            "arguments": {
                "text": SAMPLE_TEXT,
                "num_keywords": 5
            }
        })
        
        if keywords_response and "result" in keywords_response:
            result = keywords_response["result"]["content"][0]["text"]
            data = json.loads(result)
            keywords = data.get('keywords', [])
            print(f"   Top keywords: {[kw['word'] for kw in keywords[:3]]}")
        
        # Test readability analysis
        print("\n3. Testing readability analysis...")
        readability_response = self.send_request("tools/call", {
            "name": "analyze_readability",
            "arguments": {
                "text": SAMPLE_TEXT
            }
        })
        
        if readability_response and "result" in readability_response:
            result = readability_response["result"]["content"][0]["text"]
            data = json.loads(result)
            print(f"   Reading level: {data.get('reading_level', 'unknown')}")
            print(f"   Flesch score: {data.get('readability_scores', {}).get('flesch_reading_ease', 0):.1f}")
    
    def stop_server(self):
        """Stop the MCP server."""
        if self.server_process:
            print("\nStopping server...")
            self.server_process.terminate()
            
            # Wait for graceful shutdown
            try:
                self.server_process.wait(timeout=5)
                print("Server stopped successfully!")
            except subprocess.TimeoutExpired:
                print("Server didn't stop gracefully, forcing termination...")
                self.server_process.kill()
                self.server_process.wait()
                print("Server forcefully terminated!")
    
    def run_demo(self):
        """Run the complete demo."""
        print("=" * 60)
        print("Text Analysis MCP Server Demo")
        print("=" * 60)
        
        try:
            # Start server
            if not self.start_server():
                return False
            
            # Initialize server
            if not self.initialize_server():
                return False
            
            # Demo the tools
            self.demo_tools()
            
            print("\nDemo completed successfully!")
            return True
            
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
            return False
        except Exception as e:
            print(f"\nDemo failed with error: {e}")
            return False
        finally:
            self.stop_server()

if __name__ == "__main__":
    demo = MCPDemo()
    success = demo.run_demo()
    sys.exit(0 if success else 1)