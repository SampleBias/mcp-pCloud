"""
Configuration file for the pCloud MCP server.
Edit this file to configure the server behavior.
"""

import os

# pCloud API configuration
PCLOUD_API_URL = "https://api.pcloud.com"
PCLOUD_ACCESS_TOKEN = os.environ.get("PCLOUD_ACCESS_TOKEN", "")

# MCP Server configuration
SERVER_NAME = "pCloud MCP Server"
DEBUG_MODE = False
CACHE_ENABLED = True
CACHE_TTL = 300  # Cache time-to-live in seconds

# Default folder IDs
ROOT_FOLDER_ID = 0
DEFAULT_UPLOAD_FOLDER_ID = 0 