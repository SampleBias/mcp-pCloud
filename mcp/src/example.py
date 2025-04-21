"""
Example script demonstrating how to use the pCloud MCP server.

This script shows how to:
1. Create a folder
2. Upload a file to the folder
3. List the folder contents
4. Download the file
5. Share the file
6. Delete the file and folder
"""

import os
import base64
import json
import subprocess
import time
import tempfile

# Function to run a command and get JSON output
def run_mcp_command(command):
    # Format the command
    cmd = f"echo '{json.dumps(command)}' | python pcloud_mcp_server.py"
    
    # Run the command
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Parse and return the JSON result
    return json.loads(result.stdout.strip())

def main():
    print("pCloud MCP Server Example")
    print("========================\n")
    
    # Check if access token is set
    if not os.environ.get("PCLOUD_ACCESS_TOKEN"):
        print("Error: PCLOUD_ACCESS_TOKEN environment variable not set.")
        print("Please set it with: export PCLOUD_ACCESS_TOKEN='your_token'")
        return
    
    # Start a separate process for the MCP server
    server_process = subprocess.Popen(
        ["python", "pcloud_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # 1. Get account info
        print("1. Getting account info...")
        command = {
            "type": "tool",
            "tool": "get_account_info",
            "params": {}
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        print(f"Account info: {json.dumps(response, indent=2)}\n")
        
        # 2. Create a test folder
        print("2. Creating test folder...")
        command = {
            "type": "tool",
            "tool": "create_folder",
            "params": {
                "name": "MCP Test Folder",
                "parent_folder_id": 0
            }
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        folder_id = response.get("metadata", {}).get("folderid", 0)
        print(f"Created folder with ID: {folder_id}\n")
        
        # 3. Create a test file
        print("3. Creating and uploading test file...")
        test_content = "This is a test file created with the pCloud MCP server."
        test_content_base64 = base64.b64encode(test_content.encode()).decode()
        
        command = {
            "type": "tool",
            "tool": "upload_file",
            "params": {
                "file_name": "test_file.txt",
                "file_content_base64": test_content_base64,
                "folder_id": folder_id
            }
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        file_id = response.get("metadata", {}).get("fileid", 0)
        print(f"Uploaded file with ID: {file_id}\n")
        
        # 4. List folder contents
        print("4. Listing folder contents...")
        command = {
            "type": "tool",
            "tool": "list_folder",
            "params": {
                "folder_id": folder_id
            }
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        print(f"Folder contents: {json.dumps(response, indent=2)}\n")
        
        # 5. Download the file
        print("5. Downloading the file...")
        command = {
            "type": "tool",
            "tool": "download_file",
            "params": {
                "file_id": file_id
            }
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        content_base64 = response.get("content_base64", "")
        
        if content_base64:
            content = base64.b64decode(content_base64).decode()
            print(f"Downloaded file content: {content}\n")
        else:
            print("Failed to download file content\n")
        
        # 6. Share the file
        print("6. Sharing the file...")
        command = {
            "type": "tool",
            "tool": "share_item",
            "params": {
                "item_id": file_id,
                "is_folder": False
            }
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        share_link = response.get("link", "")
        print(f"File shared at: {share_link}\n")
        
        # 7. Clean up - delete file
        print("7. Cleaning up - deleting file...")
        command = {
            "type": "tool",
            "tool": "delete_item",
            "params": {
                "item_id": file_id,
                "is_folder": False
            }
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        print(f"File deletion result: {json.dumps(response, indent=2)}\n")
        
        # 8. Clean up - delete folder
        print("8. Cleaning up - deleting folder...")
        command = {
            "type": "tool",
            "tool": "delete_item",
            "params": {
                "item_id": folder_id,
                "is_folder": True
            }
        }
        server_process.stdin.write(json.dumps(command) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline().strip())
        print(f"Folder deletion result: {json.dumps(response, indent=2)}\n")
        
        print("Example completed successfully!")
        
    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main() 