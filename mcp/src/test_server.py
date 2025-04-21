#!/usr/bin/env python3
"""
Simple test script for the pCloud MCP server.
This script:
1. Checks if you have a valid pCloud token
2. Tests the get_account_info functionality
"""

import os
import sys
import json
import subprocess
import time

# Check for access token
token = os.environ.get("PCLOUD_ACCESS_TOKEN")
if not token:
    print("ERROR: PCLOUD_ACCESS_TOKEN environment variable not set.")
    print("Please run get_pcloud_token.py first to get an access token,")
    print("then set it with: export PCLOUD_ACCESS_TOKEN='your_token'")
    sys.exit(1)

print("Starting pCloud MCP server...")
# Start the server process
server_process = subprocess.Popen(
    ["python", "pcloud_mcp_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

try:
    # Test 1: Get account info
    print("\nTest 1: Getting account info...")
    command = {
        "type": "tool",
        "tool": "get_account_info",
        "params": {}
    }
    server_process.stdin.write(json.dumps(command) + "\n")
    server_process.stdin.flush()
    
    # Read response
    response_line = server_process.stdout.readline().strip()
    try:
        response = json.loads(response_line)
        print(f"Response: {json.dumps(response, indent=2)}")
        
        if "result" in response and response["result"] == 0:
            print("\n✅ SUCCESS: MCP server is working correctly!")
            print("Your pCloud account is connected.")
        else:
            print("\n❌ ERROR: Connection to pCloud failed.")
            print("Check your access token and try again.")
    except json.JSONDecodeError:
        print("\n❌ ERROR: Invalid response from server.")
        print(f"Raw response: {response_line}")
        
    # Check if there was any error
    error = server_process.stderr.readline().strip()
    if error:
        print(f"\nServer Error: {error}")

finally:
    # Clean up: terminate the server process
    print("\nShutting down MCP server...")
    server_process.terminate()
    server_process.wait()
    print("Test completed.") 