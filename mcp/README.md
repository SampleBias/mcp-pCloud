# pCloud MCP Server

This project implements a Model Context Protocol (MCP) server for pCloud, allowing AI systems to interact with your pCloud storage through a standardized interface.

## Features

- List folder contents
- Create, rename, and delete folders
- Upload and download files
- Search for files and folders
- Get file/folder metadata
- Share files and folders
- Copy and move files
- Get account information

## Prerequisites

- Python 3.7+
- A pCloud account with an OAuth access token

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pcloud-mcp.git
cd pcloud-mcp
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install mcp "mcp[cli]" requests
```

## Configuration

You need to set up your pCloud access token as an environment variable:

```bash
export PCLOUD_ACCESS_TOKEN="your_access_token_here"
```

Or on Windows:
```
set PCLOUD_ACCESS_TOKEN=your_access_token_here
```

### Getting a pCloud Access Token

1. Register your application on the [pCloud Console](https://docs.pcloud.com/oauth/index.html)
2. Implement the OAuth flow to get an access token as described in the [pCloud documentation](https://docs.pcloud.com/oauth/index.html)

## Usage

### Running the MCP Server

To start the server in development mode:

```bash
cd mcp/src
python -m mcp dev pcloud_mcp_server.py
```

### Integrating with AI Systems

This MCP server can be used with any AI system that supports the Model Context Protocol. Examples include:

- Cursor IDE
- Claude Desktop
- Custom applications built with the MCP client

### Example Flow

1. Start the MCP server
2. Connect your MCP-compatible AI application to the server
3. Ask the AI to perform operations on your pCloud storage, such as:
   - "List all files in my root folder"
   - "Upload this document to my 'Work' folder"
   - "Search for images in my 'Photos' folder"
   - "Share my presentation file with my team"

## API Reference

### Tools

| Tool | Description |
|------|-------------|
| `list_folder` | List contents of a folder |
| `create_folder` | Create a new folder |
| `rename_item` | Rename a file or folder |
| `delete_item` | Delete a file or folder |
| `get_file_link` | Get a download link for a file |
| `search` | Search for files and folders |
| `get_file_metadata` | Get metadata for a file |
| `get_folder_metadata` | Get metadata for a folder |
| `share_item` | Create a public link for sharing |
| `copy_file` | Copy a file to another folder |
| `move_item` | Move a file or folder |
| `get_account_info` | Get pCloud account information |
| `upload_file` | Upload a file to pCloud |
| `download_file` | Download a file from pCloud |

### Resources

| Resource | Description |
|----------|-------------|
| `pcloud://folder/{folder_id}` | Get contents of a folder |
| `pcloud://file/{file_id}` | Get information about a file |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 