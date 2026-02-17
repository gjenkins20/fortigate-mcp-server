"""Entry point for running FortiGate MCP server as a module.

Usage:
    python -m fortigate_mcp          # STDIO transport (for Claude Desktop)
    python -m fortigate_mcp --http   # HTTP transport
"""
import os
import sys


def main():
    config_path = os.getenv("FORTIGATE_MCP_CONFIG")
    if not config_path:
        sys.stderr.write("FORTIGATE_MCP_CONFIG environment variable must be set\n")
        sys.exit(1)

    # Check for --http flag to launch HTTP server instead
    if "--http" in sys.argv:
        from .server_http import main as http_main

        http_main()
    else:
        try:
            from .server import FortiGateMCPServer

            server = FortiGateMCPServer(config_path)
            server.start()
        except KeyboardInterrupt:
            sys.stderr.write("\nShutting down gracefully...\n")
            sys.exit(0)
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
