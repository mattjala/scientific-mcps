#!/usr/bin/env python3
"""
Demo script for the C++ Math Analysis MCP server.

This script demonstrates how to:
1. Start the C++ MCP server as a subprocess
2. Send JSON-RPC requests to the server
3. Receive and parse responses
4. Terminate the server cleanly
"""

import json
import subprocess
import time
import sys
import os

class CPPMCPDemo:
    def __init__(self):
        self.server_process = None
        
    def start_server(self):
        """Start the C++ MCP server as a subprocess."""
        print("Starting C++ Math Analysis MCP server...")
        
        # Find the server executable
        server_path = os.path.join(os.path.dirname(__file__), "build", "math_analysis_server")
        if not os.path.exists(server_path):
            print(f"Server executable not found at {server_path}")
            print("Please run: mkdir -p build && cd build && cmake .. && make")
            return False
        
        # Start the server process
        self.server_process = subprocess.Popen(
            [server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Give the server a moment to start
        time.sleep(1)
        
        if self.server_process.poll() is not None:
            stderr_output = self.server_process.stderr.read()
            print(f"Server failed to start. Error: {stderr_output}")
            return False
            
        print("Server started successfully!")
        return True
    
    def send_request(self, method, params=None):
        """Send a JSON-RPC request to the server."""
        if not hasattr(self, '_request_counter'):
            self._request_counter = 0
        self._request_counter += 1
        request_id = self._request_counter  # Use simple counter as ID
        
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
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "cpp-math-demo", "version": "1.0.0"}
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
        
        # Test statistics calculation
        print("\n1. Testing statistics calculation...")
        sample_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        
        stats_response = self.send_request("tools/call", {
            "name": "calculate_statistics",
            "arguments": {
                "data": sample_data
            }
        })
        
        if stats_response and "result" in stats_response:
            result = stats_response["result"]["structuredContent"]
            print(f"   Mean: {result.get('mean', 'N/A')}")
            print(f"   Median: {result.get('median', 'N/A')}")
            print(f"   Std Dev: {result.get('standard_deviation', 'N/A'):.3f}")
        
        # Test matrix multiplication
        print("\n2. Testing matrix multiplication...")
        matrix_a = [[1, 2], [3, 4]]
        matrix_b = [[5, 6], [7, 8]]
        
        matrix_response = self.send_request("tools/call", {
            "name": "multiply_matrices",
            "arguments": {
                "matrix_a": matrix_a,
                "matrix_b": matrix_b
            }
        })
        
        if matrix_response and "result" in matrix_response:
            result = matrix_response["result"]["structuredContent"]
            print(f"   Result matrix: {result}")
        
        # Test polynomial fitting
        print("\n3. Testing polynomial fitting...")
        x_values = [1.0, 2.0, 3.0, 4.0, 5.0]
        y_values = [2.0, 4.0, 6.0, 8.0, 10.0]  # Linear: y = 2x
        
        polyfit_response = self.send_request("tools/call", {
            "name": "polynomial_fit",
            "arguments": {
                "x_values": x_values,
                "y_values": y_values,
                "degree": 1
            }
        })
        
        if polyfit_response and "result" in polyfit_response:
            result = polyfit_response["result"]["structuredContent"]
            print(f"   Coefficients: {result.get('coefficients', 'N/A')}")
            print(f"   Equation: {result.get('equation', 'N/A')}")
        
        # Test numerical differentiation
        print("\n4. Testing numerical differentiation...")
        y_values = [1.0, 4.0, 9.0, 16.0, 25.0]  # y = x^2, dy/dx = 2x
        
        diff_response = self.send_request("tools/call", {
            "name": "numerical_differentiate",
            "arguments": {
                "y_values": y_values,
                "step_size": 1.0
            }
        })
        
        if diff_response and "result" in diff_response:
            result = diff_response["result"]["structuredContent"]
            print(f"   Derivative: {result.get('derivative', 'N/A')}")
            print(f"   Step size: {result.get('step_size', 'N/A')}")
    
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
        print("C++ Math Analysis MCP Server Demo")
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
    demo = CPPMCPDemo()
    success = demo.run_demo()
    sys.exit(0 if success else 1)