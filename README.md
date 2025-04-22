# pCloud MCP Server

A Model Context Protocol (MCP) server for pCloud integration, enabling AI systems to interact with your pCloud storage through a standardized interface.

## What is MCP?

The Model Context Protocol (MCP) provides a standard, secure, real-time, two-way communication interface for AI systems to connect with external tools, API services, and data sources.

With MCP, you can integrate your pCloud storage with AI-enabled applications like Cursor IDE and Claude Desktop, allowing them to access and manipulate your files seamlessly.

## Features

- List, search, and browse pCloud files and folders
- Create, rename, and delete folders
- Upload and download files
- Share files and folders
- Copy and move files
- Get file and folder metadata
- Access pCloud account information

## Getting Started

1. Clone this repository:
```bash
git clone https://github.com/yourusername/mcp-pCloud.git
cd mcp-pCloud
```

2. Run the setup script:
- On macOS/Linux: `./mcp/setup.sh`
- On Windows: Double-click `mcp/setup.bat`

3. Follow the prompts to:
   - Create a virtual environment
   - Install dependencies
   - Get a pCloud OAuth token
   - Start the MCP server

## Usage with AI Systems

Once your MCP server is running, you can connect it to any MCP-compatible AI system:

### Claude Desktop Configuration

To connect your pCloud MCP server to Claude Desktop:

1. Make sure your MCP server is running:
   ```bash
   cd mcp/src
   python -m mcp dev pcloud_mcp_server.py
   ```

2. Open Claude Desktop and go to Settings > Model Context Protocol

3. Click "Add New Connection" and enter:
   - **Name**: pCloud Storage
   - **Transport Type**: HTTP
   - **URL**: http://localhost:8000
   - **Description** (optional): Access to my pCloud files and folders
   - **Icon** (optional): 📁 or 🗂️

4. Save and enable the connection

5. In your conversations with Claude, you can now ask to:
   - "Show me files in my pCloud account"
   - "Upload this document to my pCloud"
   - "Find all images in my pCloud storage"
   - "Share this file with my team"

### Cursor IDE Configuration

For Cursor IDE:

1. Start your MCP server as above
2. Open Cursor IDE
3. Access the MCP configuration in settings
4. Add a new connection to http://localhost:8000
5. Use Cursor's AI features to interact with your pCloud files directly

## Documentation

For detailed documentation, see the [mcp/README.md](mcp/README.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
