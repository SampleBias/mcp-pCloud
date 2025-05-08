# fastmcp.py
import sys

class FastMCP:
    def __init__(self, server_name="FastMCP Server"):
        self.server_name = server_name
        self.tools = {}
        self.resources = {}

    def tool(self):
        # Decorator for registering a tool
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator

    def resource(self, uri_template):
        # Decorator for registering a resource
        def decorator(func):
            self.resources[uri_template] = func
            return func
        return decorator

    def run(self, transport="stdio", host="127.0.0.1", port=8000):
        # Minimal stub for stdio transport
        print(f"FastMCP server '{self.server_name}' started with transport={transport}", file=sys.stderr)
        if transport == "stdio":
            # In a real implementation, this would handle stdio communication.
            # For now, just keep the process alive.
            try:
                while True:
                    line = sys.stdin.readline()
                    if not line:
                        break
            except KeyboardInterrupt:
                print("FastMCP server stopped.", file=sys.stderr)
        elif transport == "http":
            # In a real implementation, this would start an HTTP server.
            print("HTTP transport is not implemented in this stub.", file=sys.stderr)
        else:
            print(f"Unknown transport: {transport}", file=sys.stderr)
