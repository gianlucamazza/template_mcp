"""Server implementation for the Template MCP."""

import logging
from typing import Literal, Optional
from fastmcp import FastMCP
from template_mcp.config import ServerConfig

logger = logging.getLogger(__name__)


class TemplateMCPServer:
    """Template Model Context Protocol Server."""

    def __init__(self, config: ServerConfig):
        """Initialize the MCP server.

        Args:
            config: Server configuration
        """
        self.config = config
        self.server: FastMCP = FastMCP(log_level="DEBUG" if config.debug else "INFO")

    async def start(self):
        """Start the server."""
        logger.info("Starting Template MCP server")
        await self.server.start()


def create_server(config: ServerConfig) -> FastMCP:
    """Create a new MCP server instance.
    
    Args:
        config: Server configuration
        
    Returns:
        A configured FastMCP server
    """
    server: FastMCP = FastMCP(log_level="DEBUG" if config.debug else "INFO")
    logger.info("Created new FastMCP server")
    return server


def run_server(server: FastMCP, transport: str = "stdio"):
    """Run the server with the specified transport.
    
    Args:
        server: The FastMCP server instance
        transport: Transport protocol to use (stdio or sse)
    """
    # Use the appropriate transport type
    transport_type: Optional[Literal['stdio', 'sse']] = 'stdio' if transport == 'stdio' else 'sse'
    server.run(transport=transport_type)


def main() -> None:
    """Main entry point for the package."""
    # Create and run the server
    from template_mcp.config import ServerConfig
    config = ServerConfig(debug=True)
    server = create_server(config)
    run_server(server)


if __name__ == "__main__":
    main() 