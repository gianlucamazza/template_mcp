"""Template MCP server implementation."""

import asyncio
from . import server
from . import tools
from . import resources
from . import prompts

__version__ = "0.1.0"


def main():
    """Main entry point for the package."""
    asyncio.run(server.main())


__all__ = ["main", "server", "tools", "resources", "prompts"] 