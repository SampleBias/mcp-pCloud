#!/bin/bash

# Script to set up and run the pCloud MCP server

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install mcp "mcp[cli]" requests

# Check if PCLOUD_ACCESS_TOKEN is set
if [ -z "$PCLOUD_ACCESS_TOKEN" ]; then
    echo "Warning: PCLOUD_ACCESS_TOKEN environment variable is not set."
    echo "You will need to set this to use the MCP server."
    echo "You can get a token by running: python src/get_pcloud_token.py"
    
    # Prompt to run the token script
    read -p "Do you want to get a pCloud access token now? (y/n): " GET_TOKEN
    if [ "$GET_TOKEN" = "y" ] || [ "$GET_TOKEN" = "Y" ]; then
        # Edit get_pcloud_token.py to set client ID and secret
        echo "Please edit src/get_pcloud_token.py to set your CLIENT_ID and CLIENT_SECRET before continuing."
        read -p "Press enter when ready..."
        
        # Run the token script
        python src/get_pcloud_token.py
        
        # If token file exists, offer to set it
        if [ -f "src/pcloud_token.txt" ]; then
            TOKEN=$(grep "Access Token:" src/pcloud_token.txt | cut -d' ' -f3)
            if [ ! -z "$TOKEN" ]; then
                export PCLOUD_ACCESS_TOKEN="$TOKEN"
                echo "Access token set for this session."
                echo "To set it permanently, add the following to your ~/.bashrc or ~/.zshrc file:"
                echo "export PCLOUD_ACCESS_TOKEN=\"$TOKEN\""
            fi
        fi
    fi
fi

# Offer to run the server
read -p "Do you want to start the MCP server now? (y/n): " START_SERVER
if [ "$START_SERVER" = "y" ] || [ "$START_SERVER" = "Y" ]; then
    echo "Starting the MCP server..."
    cd src
    python -m mcp dev pcloud_mcp_server.py
else
    echo "To start the server later, run:"
    echo "  source venv/bin/activate"
    echo "  cd src"
    echo "  python -m mcp dev pcloud_mcp_server.py"
fi 