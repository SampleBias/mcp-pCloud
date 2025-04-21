from mcp.server.fastmcp import FastMCP
import requests
import os
import json
import tempfile
import base64
from typing import Dict, List, Optional, Any, Union

# Instantiate an MCP server client
mcp = FastMCP("pCloud MCP Server")

# pCloud API base URL
PCLOUD_API_URL = "https://api.pcloud.com"

# Make sure to get your access token from pCloud OAuth
# and set it as an environment variable or provide it directly
ACCESS_TOKEN = os.environ.get("PCLOUD_ACCESS_TOKEN", "")

def api_request(endpoint: str, params: Dict = None, method: str = "GET", files: Dict = None):
    """Make an API request to pCloud"""
    if params is None:
        params = {}
    
    # Add access token to params
    params["access_token"] = ACCESS_TOKEN
    
    url = f"{PCLOUD_API_URL}/{endpoint}"
    
    if method.upper() == "GET":
        response = requests.get(url, params=params)
    elif method.upper() == "POST":
        if files:
            response = requests.post(url, params=params, files=files)
        else:
            response = requests.post(url, params=params)
    
    return response.json()

# Define MCP tools for pCloud operations

@mcp.tool()
def list_folder(folder_id: int = 0) -> Dict:
    """
    List contents of a folder in pCloud
    
    Args:
        folder_id: The ID of the folder to list (default: 0 for root)
        
    Returns:
        Dictionary containing folder contents
    """
    result = api_request("listfolder", {"folderid": folder_id})
    return result

@mcp.tool()
def create_folder(name: str, parent_folder_id: int = 0) -> Dict:
    """
    Create a new folder in pCloud
    
    Args:
        name: Name of the folder to create
        parent_folder_id: ID of the parent folder (default: 0 for root)
        
    Returns:
        Dictionary containing created folder metadata
    """
    result = api_request("createfolder", {
        "name": name,
        "folderid": parent_folder_id
    })
    return result

@mcp.tool()
def rename_item(item_id: int, name: str, is_folder: bool = False) -> Dict:
    """
    Rename a file or folder in pCloud
    
    Args:
        item_id: ID of the file or folder to rename
        name: New name for the item
        is_folder: Whether the item is a folder (True) or file (False)
        
    Returns:
        Dictionary containing result of the operation
    """
    params = {"name": name}
    
    if is_folder:
        params["folderid"] = item_id
        endpoint = "renamefolder"
    else:
        params["fileid"] = item_id
        endpoint = "renamefile"
    
    result = api_request(endpoint, params)
    return result

@mcp.tool()
def delete_item(item_id: int, is_folder: bool = False) -> Dict:
    """
    Delete a file or folder in pCloud
    
    Args:
        item_id: ID of the file or folder to delete
        is_folder: Whether the item is a folder (True) or file (False)
        
    Returns:
        Dictionary containing result of the operation
    """
    params = {}
    
    if is_folder:
        params["folderid"] = item_id
        endpoint = "deletefolder"
    else:
        params["fileid"] = item_id
        endpoint = "deletefile"
    
    result = api_request(endpoint, params)
    return result

@mcp.tool()
def get_file_link(file_id: int) -> Dict:
    """
    Get a download link for a file
    
    Args:
        file_id: ID of the file to get a link for
        
    Returns:
        Dictionary containing download link
    """
    result = api_request("getfilelink", {"fileid": file_id})
    return result

@mcp.tool()
def search(query: str, folder_id: int = 0) -> Dict:
    """
    Search for files and folders in pCloud
    
    Args:
        query: Search query
        folder_id: ID of the folder to search in (default: 0 for root)
        
    Returns:
        Dictionary containing search results
    """
    result = api_request("search", {
        "query": query,
        "folderid": folder_id
    })
    return result

@mcp.tool()
def get_file_metadata(file_id: int) -> Dict:
    """
    Get metadata for a file
    
    Args:
        file_id: ID of the file
        
    Returns:
        Dictionary containing file metadata
    """
    result = api_request("stat", {"fileid": file_id})
    return result

@mcp.tool()
def get_folder_metadata(folder_id: int) -> Dict:
    """
    Get metadata for a folder
    
    Args:
        folder_id: ID of the folder
        
    Returns:
        Dictionary containing folder metadata
    """
    result = api_request("stat", {"folderid": folder_id})
    return result

@mcp.tool()
def share_item(item_id: int, is_folder: bool = False) -> Dict:
    """
    Create a public link for sharing a file or folder
    
    Args:
        item_id: ID of the file or folder to share
        is_folder: Whether the item is a folder (True) or file (False)
        
    Returns:
        Dictionary containing public link information
    """
    params = {}
    
    if is_folder:
        params["folderid"] = item_id
    else:
        params["fileid"] = item_id
    
    result = api_request("getfilepublink" if not is_folder else "getfolderpublink", params)
    return result

@mcp.tool()
def copy_file(file_id: int, dest_folder_id: int) -> Dict:
    """
    Copy a file to another folder
    
    Args:
        file_id: ID of the file to copy
        dest_folder_id: ID of the destination folder
        
    Returns:
        Dictionary containing result of the operation
    """
    result = api_request("copyfile", {
        "fileid": file_id,
        "tofolderid": dest_folder_id
    })
    return result

@mcp.tool()
def move_item(item_id: int, dest_folder_id: int, is_folder: bool = False) -> Dict:
    """
    Move a file or folder to another folder
    
    Args:
        item_id: ID of the item to move
        dest_folder_id: ID of the destination folder
        is_folder: Whether the item is a folder (True) or file (False)
        
    Returns:
        Dictionary containing result of the operation
    """
    params = {"tofolderid": dest_folder_id}
    
    if is_folder:
        params["folderid"] = item_id
        endpoint = "renamefolder"
    else:
        params["fileid"] = item_id
        endpoint = "renamefile"
    
    result = api_request(endpoint, params)
    return result

@mcp.tool()
def get_account_info() -> Dict:
    """
    Get pCloud account information
    
    Returns:
        Dictionary containing account information
    """
    result = api_request("userinfo")
    return result

@mcp.tool()
def upload_file(file_name: str, file_content_base64: str, folder_id: int = 0) -> Dict:
    """
    Upload a file to pCloud
    
    Args:
        file_name: Name to save the file as
        file_content_base64: Base64-encoded content of the file
        folder_id: ID of the folder to upload to (default: 0 for root)
        
    Returns:
        Dictionary containing upload result
    """
    # Decode base64 content
    file_content = base64.b64decode(file_content_base64)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_content)
        temp_path = temp_file.name
    
    try:
        # Prepare the upload
        params = {
            "folderid": folder_id,
            "access_token": ACCESS_TOKEN
        }
        
        url = f"{PCLOUD_API_URL}/uploadfile"
        
        # Upload the file
        with open(temp_path, "rb") as f:
            files = {"file": (file_name, f)}
            response = requests.post(url, params=params, files=files)
        
        # Return the result
        return response.json()
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@mcp.tool()
def download_file(file_id: int) -> Dict:
    """
    Download a file from pCloud and return its content as base64
    
    Args:
        file_id: ID of the file to download
        
    Returns:
        Dictionary containing file metadata and base64-encoded content
    """
    # First get the file link
    link_result = api_request("getfilelink", {"fileid": file_id})
    
    if "error" in link_result and link_result["error"] != 0:
        return link_result
    
    # Get the file metadata
    metadata = api_request("stat", {"fileid": file_id})
    
    if "error" in metadata and metadata["error"] != 0:
        return metadata
    
    # Build the actual download URL
    hosts = link_result.get("hosts", [])
    path = link_result.get("path", "")
    
    if not hosts or not path:
        return {"error": 1000, "message": "Invalid file link response"}
    
    download_url = f"https://{hosts[0]}{path}"
    
    # Download the file
    response = requests.get(download_url)
    
    if response.status_code != 200:
        return {"error": response.status_code, "message": "Failed to download file"}
    
    # Encode file content as base64
    content_base64 = base64.b64encode(response.content).decode("utf-8")
    
    # Return metadata and content
    return {
        "metadata": metadata,
        "content_base64": content_base64
    }

@mcp.resource("pcloud://folder/{folder_id}")
def get_folder_contents(folder_id: str) -> Dict:
    """
    Get contents of a folder as a resource
    
    Args:
        folder_id: ID of the folder
        
    Returns:
        Dictionary containing folder contents
    """
    result = api_request("listfolder", {"folderid": int(folder_id)})
    return result

@mcp.resource("pcloud://file/{file_id}")
def get_file_info(file_id: str) -> Dict:
    """
    Get information about a file as a resource
    
    Args:
        file_id: ID of the file
        
    Returns:
        Dictionary containing file information
    """
    result = api_request("stat", {"fileid": int(file_id)})
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio") 