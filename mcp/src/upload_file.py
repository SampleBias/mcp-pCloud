import requests
import os
import sys
from typing import Dict, Optional

# pCloud API base URL
PCLOUD_API_URL = "https://api.pcloud.com"

def upload_file(file_path: str, folder_id: int = 0, access_token: Optional[str] = None) -> Dict:
    """
    Upload a file to pCloud
    
    Args:
        file_path: Path to the file to upload
        folder_id: ID of the folder to upload to (default: 0 for root)
        access_token: pCloud access token (will use env var if not provided)
        
    Returns:
        Dictionary containing upload result
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get access token from env var if not provided
    if access_token is None:
        access_token = os.environ.get("PCLOUD_ACCESS_TOKEN")
        if not access_token:
            raise ValueError("No access token provided and PCLOUD_ACCESS_TOKEN env var not set")
    
    url = f"{PCLOUD_API_URL}/uploadfile"
    
    params = {
        "folderid": folder_id,
        "access_token": access_token
    }
    
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        response = requests.post(url, params=params, files=files)
    
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_file.py <file_path> [folder_id]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    folder_id = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    
    try:
        result = upload_file(file_path, folder_id)
        print(f"File uploaded successfully: {result}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        sys.exit(1) 