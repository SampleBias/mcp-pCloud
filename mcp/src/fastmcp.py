import sys
import json

class FastMCP:
    def __init__(self, server_name="FastMCP Server"):
        self.server_name = server_name
        self.tools = {}
        self.resources = {}

    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator

    def resource(self, uri_template):
        def decorator(func):
            self.resources[uri_template] = func
            return func
        return decorator

    def run(self, transport="stdio", host="127.0.0.1", port=8000):
        print(f"FastMCP server '{self.server_name}' started with transport={transport}", file=sys.stderr)
        if transport == "stdio":
            try:
                while True:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    try:
                        request = json.loads(line)
                        # Respond to 'initialize' with a minimal valid response
                        if request.get("method") == "initialize":
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {
                                    "serverInfo": {
                                        "name": self.server_name,
                                        "version": "0.1.0"
                                    },
                                    "capabilities": {}
                                }
                            }
                            print(json.dumps(response), flush=True)
                        # Add more handlers for other methods as needed
                    except Exception as e:
                        print(f"Error handling request: {e}", file=sys.stderr)
            except KeyboardInterrupt:
                print("FastMCP server stopped.", file=sys.stderr)
        elif transport == "http":
            print("HTTP transport is not implemented in this stub.", file=sys.stderr)
        else:
            print(f"Unknown transport: {transport}", file=sys.stderr)
