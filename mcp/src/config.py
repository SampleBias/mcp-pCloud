"""
Configuration file for the pCloud MCP server.
Edit this file to configure the server behavior.
"""

import os

# pCloud API configuration
PCLOUD_API_URL = "https://api.pcloud.com"

# Authentication options
# Option 1: Use direct access token (legacy approach)
PCLOUD_ACCESS_TOKEN = os.environ.get("PCLOUD_ACCESS_TOKEN", "")

# Option 2: Use email/password authentication
# Fill these in to use login functionality instead of direct token
PCLOUD_EMAIL = os.environ.get("PCLOUD_EMAIL", "")  # Your pCloud email
PCLOUD_PASSWORD = os.environ.get("PCLOUD_PASSWORD", "")  # Your pCloud password

# Token configuration
TOKEN_EXPIRE_SECONDS = 86400 * 30  # 30 days by default
TOKEN_INACTIVE_EXPIRE_SECONDS = 86400 * 7  # 7 days of inactivity by default
DEVICE_NAME = os.environ.get("DEVICE_NAME", "pCloud MCP Client")
USE_SSL = True  # Set to False to use digest authentication for non-HTTPS connections

# Auto-login at startup (only if email and password are provided)
AUTO_LOGIN = True

# MCP Server configuration
SERVER_NAME = "pCloud MCP Server"
DEBUG_MODE = False
CACHE_ENABLED = True
CACHE_TTL = 300  # Cache time-to-live in seconds

# Default folder IDs
ROOT_FOLDER_ID = 0
DEFAULT_UPLOAD_FOLDER_ID = 0 