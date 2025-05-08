from mcp.server.fastmcp import FastMCP
import requests
import os
import json
import tempfile
import base64
import hashlib
from typing import Dict, List, Optional, Any, Union

# Import configuration
try:
    from config import *
except ImportError:
    # Default configuration if config.py is missing
    PCLOUD_API_URL = "https://api.pcloud.com"
    PCLOUD_ACCESS_TOKEN = os.environ.get("PCLOUD_ACCESS_TOKEN", "")
    PCLOUD_EMAIL = os.environ.get("PCLOUD_EMAIL", "")
    PCLOUD_PASSWORD = os.environ.get("PCLOUD_PASSWORD", "")
    TOKEN_EXPIRE_SECONDS = 86400 * 30  # 30 days
    TOKEN_INACTIVE_EXPIRE_SECONDS = 86400 * 7  # 7 days
    DEVICE_NAME = os.environ.get("DEVICE_NAME", "pCloud MCP Client")
    USE_SSL = True
    AUTO_LOGIN = True
    SERVER_NAME = "pCloud MCP Server"
    DEBUG_MODE = False
    CACHE_ENABLED = False
    ROOT_FOLDER_ID = 0
    DEFAULT_UPLOAD_FOLDER_ID = 0

# Instantiate an MCP server client
mcp = FastMCP(SERVER_NAME)

# Use the access token from config
ACCESS_TOKEN = PCLOUD_ACCESS_TOKEN

# Debug information
if DEBUG_MODE:
    print(f"Starting {SERVER_NAME}")
    print(f"API URL: {PCLOUD_API_URL}")
    print(f"Access token set: {'Yes' if ACCESS_TOKEN else 'No'}")
    print(f"Email configured: {'Yes' if PCLOUD_EMAIL else 'No'}")

def api_request(endpoint: str, params: Dict = None, method: str = "GET", files: Dict = None, use_auth: bool = True):
    """Make an API request to pCloud"""
    if params is None:
        params = {}
    
    # Add access token to params if authentication is required and token is available
    if use_auth and ACCESS_TOKEN:
        params["auth"] = ACCESS_TOKEN
    
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
def login(username: str, password: str, use_ssl: bool = True) -> Dict:
    """
    Login to pCloud and get authentication token
    
    Args:
        username: Email of the user
        password: Password of the user
        use_ssl: Whether to use SSL (direct password) or digest authentication
        
    Returns:
        Dictionary containing authentication result including token
    """
    global ACCESS_TOKEN
    
    if use_ssl:
        # Direct username/password authentication (should be used over HTTPS)
        result = api_request("userinfo", {
            "getauth": 1,
            "logout": 1,
            "username": username,
            "password": password
        }, use_auth=False)
    else:
        # Digest authentication for non-SSL connections
        # Step 1: Get digest
        digest_result = api_request("getdigest", use_auth=False)
        
        if "error" in digest_result and digest_result["error"] != 0:
            return digest_result
        
        digest = digest_result.get("digest", "")
        
        # Step 2: Calculate password digest
        # passworddigest = sha1(password + sha1(lowercase(username)) + digest)
        username_hash = hashlib.sha1(username.lower().encode()).hexdigest()
        password_digest = hashlib.sha1((password + username_hash + digest).encode()).hexdigest()
        
        # Step 3: Login with digest
        result = api_request("userinfo", {
            "getauth": 1,
            "logout": 1,
            "username": username,
            "digest": digest,
            "passworddigest": password_digest
        }, use_auth=False)
    
    # Update the access token if login was successful
    if "auth" in result and result.get("result", -1) == 0:
        ACCESS_TOKEN = result["auth"]
    
    return result

@mcp.tool()
def login_advanced(username: str, password: str, expire_seconds: int = None, 
                  inactive_expire_seconds: int = None, device_name: str = None,
                  use_ssl: bool = True) -> Dict:
    """
    Advanced login to pCloud with custom token expiration parameters
    
    Args:
        username: Email of the user
        password: Password of the user
        expire_seconds: Token absolute expiration time in seconds from now
        inactive_expire_seconds: Token expiration time after inactivity in seconds
        device_name: Name of the device requesting authorization
        use_ssl: Whether to use SSL (direct password) or digest authentication
        
    Returns:
        Dictionary containing authentication result including token
    """
    global ACCESS_TOKEN
    
    # Prepare parameters
    params = {
        "getauth": 1,
        "logout": 1,
        "username": username
    }
    
    if expire_seconds is not None:
        params["authexpire"] = expire_seconds
    
    if inactive_expire_seconds is not None:
        params["authinactiveexpire"] = inactive_expire_seconds
    
    if device_name is not None:
        params["device"] = device_name
    
    if use_ssl:
        # Direct username/password authentication (should be used over HTTPS)
        params["password"] = password
        result = api_request("userinfo", params, use_auth=False)
    else:
        # Digest authentication for non-SSL connections
        # Step 1: Get digest
        digest_result = api_request("getdigest", use_auth=False)
        
        if "error" in digest_result and digest_result["error"] != 0:
            return digest_result
        
        digest = digest_result.get("digest", "")
        
        # Step 2: Calculate password digest
        # passworddigest = sha1(password + sha1(lowercase(username)) + digest)
        username_hash = hashlib.sha1(username.lower().encode()).hexdigest()
        password_digest = hashlib.sha1((password + username_hash + digest).encode()).hexdigest()
        
        # Step 3: Login with digest
        params["digest"] = digest
        params["passworddigest"] = password_digest
        result = api_request("userinfo", params, use_auth=False)
    
    # Update the access token if login was successful
    if "auth" in result and result.get("result", -1) == 0:
        ACCESS_TOKEN = result["auth"]
    
    return result

@mcp.tool()
def logout() -> Dict:
    """
    Logout from pCloud (invalidate the current authentication token)
    
    Returns:
        Dictionary containing logout result
    """
    global ACCESS_TOKEN
    
    if not ACCESS_TOKEN:
        return {"result": 0, "message": "Not logged in"}
    
    result = api_request("logout")
    
    # Clear the access token if logout was successful
    if result.get("result", -1) == 0:
        ACCESS_TOKEN = ""
    
    return result

@mcp.tool()
def list_tokens() -> Dict:
    """
    List all active authentication tokens for the current user
    
    Returns:
        Dictionary containing token information
    """
    result = api_request("listtoken")
    return result

@mcp.tool()
def delete_token(token_id: str) -> Dict:
    """
    Delete/invalidate a specific authentication token
    
    Args:
        token_id: ID of the token to delete
        
    Returns:
        Dictionary containing operation result
    """
    result = api_request("deletetoken", {"tokenid": token_id})
    return result

@mcp.tool()
def set_token_expiration(token_id: str, expire_seconds: int = None, inactive_expire_seconds: int = None) -> Dict:
    """
    Set expiration parameters for a specific token
    
    Args:
        token_id: ID of the token to modify
        expire_seconds: Seconds until token expires (absolute)
        inactive_expire_seconds: Seconds of inactivity until token expires
        
    Returns:
        Dictionary containing operation result
    """
    params = {"tokenid": token_id}
    
    if expire_seconds is not None:
        params["expire"] = expire_seconds
    
    if inactive_expire_seconds is not None:
        params["expireinactive"] = inactive_expire_seconds
    
    result = api_request("changetokenexpire", params)
    return result

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
            "folderid": folder_id
        }
        
        if ACCESS_TOKEN:
            params["auth"] = ACCESS_TOKEN
        
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

# Auto-login if configured
if AUTO_LOGIN and PCLOUD_EMAIL and PCLOUD_PASSWORD and not ACCESS_TOKEN:
    if DEBUG_MODE:
        print("Attempting auto-login with configured credentials...")
    try:
        login_result = login_advanced(
            username=PCLOUD_EMAIL,
            password=PCLOUD_PASSWORD,
            expire_seconds=TOKEN_EXPIRE_SECONDS,
            inactive_expire_seconds=TOKEN_INACTIVE_EXPIRE_SECONDS,
            device_name=DEVICE_NAME,
            use_ssl=USE_SSL
        )
        if login_result.get("result", -1) == 0 and "auth" in login_result:
            if DEBUG_MODE:
                print("Auto-login successful")
        else:
            if DEBUG_MODE:
                print(f"Auto-login failed: {login_result.get('error', 'Unknown error')}")
    except Exception as e:
        if DEBUG_MODE:
            print(f"Auto-login exception: {str(e)}")

if __name__ == "__main__":
    mcp.run(transport="stdio") 