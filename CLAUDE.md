# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FortiGate MCP Server — a Model Context Protocol server for managing FortiGate network devices via their REST API. Exposes ~30 tools across 5 categories (device, firewall, network, routing, virtual IP). Supports both STDIO and HTTP transports.

## Common Commands

```bash
# Install dependencies (with dev extras)
pip install -e ".[dev]"

# Run unit tests (enforces 80% coverage minimum)
pytest

# Run a single test file
pytest tests/test_tools.py

# Run a specific test
pytest tests/test_tools.py::TestClassName::test_method_name

# Linting & formatting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/

# Security scanning
bandit -r src/ --skip B101,B601
safety check

# Start STDIO server
FORTIGATE_MCP_CONFIG=config/config.json python -m src.fortigate_mcp.server

# Start HTTP server
python -m src.fortigate_mcp.server_http --host 0.0.0.0 --port 8814 --path /fortigate-mcp --config config/config.json

# Integration tests (requires running HTTP server on port 8814)
python integration_tests.py

# Docker
docker compose up --build
```

## Architecture

### Dual Server Entry Points

- **`src/fortigate_mcp/server.py`** — `FortiGateMCPServer`: STDIO transport, fully async. Config via `FORTIGATE_MCP_CONFIG` env var. Runs with `anyio` + `mcp.run_stdio_async()`.
- **`src/fortigate_mcp/server_http.py`** — `FortiGateMCPHTTPServer`: HTTP transport, sync method wrappers. Runs with FastAPI + uvicorn on port 8814. Accepts CLI args.

Both servers share the same initialization pattern: load config → setup logging → create `FortiGateManager` → instantiate tool classes → register tools with `FastMCP` via `@mcp.tool()` decorators.

### Module Layout

- **`config/`** — Pydantic models (`models.py`) and config loader (`loader.py`). Root `Config` contains `ServerConfig`, `FortiGateConfig` (dict of devices), `AuthConfig`, `LoggingConfig`, `RateLimitConfig`. Config loaded from JSON file path.
- **`core/fortigate.py`** — `FortiGateAPI` (single device client using `httpx`, base URL `https://{host}:{port}/api/v2`) and `FortiGateManager` (multi-device registry). Auth: Bearer token or HTTP Basic.
- **`core/logging.py`** — `setup_logging()`, `get_logger(name)` (prefixed `fortigate-mcp.{name}`), helper functions `log_api_call()` and `log_tool_call()`.
- **`tools/`** — Each category is a class inheriting `FortiGateTool` (in `base.py`). Base provides `_get_device_api()`, `_format_response()`, `_handle_error()`, `_execute_with_logging()`. Tool descriptions live in `definitions.py` as constants.
- **`formatting/`** — `FortiGateFormatters` (static methods converting API data to markdown) and `FortiGateTemplates` (text templates). All tools return `List[Content]` (MCP `TextContent`).

### Key Patterns

- **Tool registration**: Tool classes implement methods; the server classes register them as closures via `@self.mcp.tool(description=...)` in `_setup_tools()`.
- **Device resolution**: Every tool takes a `device_id` string → `FortiGateManager.get_device()` → `FortiGateAPI` instance. Most also accept optional `vdom`.
- **Error handling**: `FortiGateAPIError` carries HTTP status codes. `FortiGateTool._handle_error()` maps status codes to user-friendly messages.
- **Return type**: All MCP tools return `List[Content]` where Content is `mcp.types.TextContent`.

## Code Style

- **Black** with 88-char line length, Python 3.11 target
- **isort** with "black" profile
- **mypy** strict mode (relaxed for tests: `disallow_untyped_defs = false`)
- **bandit** skips: B101 (assert), B601 (paramiko)

## Test Markers

```bash
pytest -m unit        # Unit tests only
pytest -m integration # Integration tests only
pytest -m slow        # Slow tests only
```

## Configuration

Device config requires `host` + either `api_token` or `username`/`password`. See `config/config.example.json` for full schema. Cursor IDE integration examples in `examples/cursor_mcp_config.json`.
