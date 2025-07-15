#!/usr/bin/env python3
import json
import subprocess
import time

# Test with simpler JSON
server_path = "./build/math_analysis_server"
server_process = subprocess.Popen(
    [server_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Simple initialize request
simple_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "clientInfo": {"name": "test", "version": "1.0.0"}
    }
}

request_json = json.dumps(simple_request) + "\n"
print(f"Sending: {request_json.strip()}")

server_process.stdin.write(request_json)
server_process.stdin.flush()

response_line = server_process.stdout.readline()
print(f"Response: {response_line.strip()}")

# Test tools/list
tools_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}

request_json = json.dumps(tools_request) + "\n"
print(f"Sending: {request_json.strip()}")

server_process.stdin.write(request_json)
server_process.stdin.flush()

response_line = server_process.stdout.readline()
print(f"Response: {response_line.strip()}")

# Test calculate_statistics
stats_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "calculate_statistics",
        "arguments": {
            "data": [1.0, 2.0, 3.0, 4.0, 5.0]
        }
    }
}

request_json = json.dumps(stats_request) + "\n"
print(f"Sending: {request_json.strip()}")

server_process.stdin.write(request_json)
server_process.stdin.flush()

response_line = server_process.stdout.readline()
print(f"Response: {response_line.strip()}")

server_process.terminate()
server_process.wait()