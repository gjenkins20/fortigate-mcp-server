"""Core functionality for FortiGate MCP."""

from .fortigate import FortiGateManager
from .logging import setup_logging

__all__ = ["setup_logging", "FortiGateManager"]
