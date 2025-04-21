"""
Script to help users get an OAuth token from pCloud.

This script creates a simple web server that handles the OAuth flow with pCloud.
"""

import os
import sys
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json

# pCloud OAuth configuration
# You can set these directly here or enter them when prompted
CLIENT_ID = os.environ.get("PCLOUD_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("PCLOUD_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:8000/oauth/callback"
PCLOUD_AUTH_URL = "https://my.pcloud.com/oauth2/authorize"
PCLOUD_TOKEN_URL = "https://api.pcloud.com/oauth2_token"

# Scopes needed for the MCP server
SCOPES = "read_file,write_file,delete_file,create_folder,delete_folder,rename_folder"

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests to the callback URL"""
        
        # Parse the query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Check if the path is the callback path
        if parsed_path.path == "/oauth/callback":
            # Check if there's an authorization code
            if "code" in query_params:
                code = query_params["code"][0]
                
                # Exchange the code for an access token
                token_response = requests.post(PCLOUD_TOKEN_URL, data={
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": REDIRECT_URI
                })
                
                token_data = token_response.json()
                
                # Prepare the response
                if "access_token" in token_data:
                    access_token = token_data["access_token"]
                    response_html = f"""
                    <html>
                    <head><title>pCloud OAuth Token</title></head>
                    <body>
                        <h1>OAuth Token Received</h1>
                        <p>Your pCloud access token is:</p>
                        <pre>{access_token}</pre>
                        <p>Please save this token securely and set it as the <code>PCLOUD_ACCESS_TOKEN</code> environment variable.</p>
                        <p>You can now close this window.</p>
                    </body>
                    </html>
                    """
                    
                    # Save the token to a file
                    with open("pcloud_token.txt", "w") as f:
                        f.write(f"Access Token: {access_token}\n")
                        if "userid" in token_data:
                            f.write(f"User ID: {token_data['userid']}\n")
                        if "expires_in" in token_data:
                            f.write(f"Expires In: {token_data['expires_in']} seconds\n")
                    
                    print("\nAccess token received and saved to pcloud_token.txt")
                    print(f"Access Token: {access_token}")
                    print("\nSet this as your PCLOUD_ACCESS_TOKEN environment variable:")
                    print(f"export PCLOUD_ACCESS_TOKEN=\"{access_token}\"")
                else:
                    response_html = f"""
                    <html>
                    <head><title>pCloud OAuth Error</title></head>
                    <body>
                        <h1>OAuth Error</h1>
                        <p>Failed to get access token:</p>
                        <pre>{json.dumps(token_data, indent=2)}</pre>
                    </body>
                    </html>
                    """
                    print("\nError getting access token:")
                    print(json.dumps(token_data, indent=2))
            else:
                # Handle errors
                error = query_params.get("error", ["Unknown error"])[0]
                error_description = query_params.get("error_description", ["No description"])[0]
                
                response_html = f"""
                <html>
                <head><title>pCloud OAuth Error</title></head>
                <body>
                    <h1>OAuth Error</h1>
                    <p>Error: {error}</p>
                    <p>Description: {error_description}</p>
                </body>
                </html>
                """
                print(f"\nError: {error}")
                print(f"Description: {error_description}")
        else:
            # Handle other paths
            response_html = """
            <html>
            <head><title>pCloud OAuth</title></head>
            <body>
                <h1>pCloud OAuth Server</h1>
                <p>This is the OAuth server for pCloud integration.</p>
            </body>
            </html>
            """
        
        # Send the response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response_html.encode())
        
        # Signal that we're done
        self.server.oauth_complete = True

def main():
    global CLIENT_ID, CLIENT_SECRET
    
    # Prompt for CLIENT_ID and CLIENT_SECRET if not set
    if not CLIENT_ID:
        CLIENT_ID = input("Enter your pCloud Client ID: ")
    
    if not CLIENT_SECRET:
        CLIENT_SECRET = input("Enter your pCloud Client Secret: ")
    
    # Check if client ID and secret are set
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: CLIENT_ID and CLIENT_SECRET are required.")
        print("You can get these from the pCloud Console after registering your app.")
        return
    
    # Create the OAuth URL
    auth_url = f"{PCLOUD_AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    
    # Start the HTTP server
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)
    httpd.oauth_complete = False
    
    print("Starting OAuth flow...")
    print(f"Opening browser to authorize at {auth_url}")
    
    # Open the browser
    webbrowser.open(auth_url)
    
    print("\nWaiting for authorization...")
    
    # Run the server until OAuth is complete
    while not httpd.oauth_complete:
        httpd.handle_request()
    
    print("\nOAuth flow completed. You can now use the pCloud MCP server.")

if __name__ == "__main__":
    main() 