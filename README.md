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

1. In your AI application, look for MCP integration settings
2. Connect to your local MCP server (usually running on http://localhost:8000)
3. Ask the AI to interact with your pCloud storage:
   - "Show me files in my pCloud account"
   - "Upload this document to my pCloud"
   - "Find all images in my pCloud storage"
   - "Share this file with my team"

## Documentation

For detailed documentation, see the [mcp/README.md](mcp/README.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
