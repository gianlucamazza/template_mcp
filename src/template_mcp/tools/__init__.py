"""Tools module for MCP server."""

import logging
from typing import Union
from ..config import ServerConfig
from .example_tool import register_tools

logger = logging.getLogger(__name__)


def setup_tools(server, config: Union[ServerConfig, None] = None) -> None:
    """Set up all tools for the server.
    
    Args:
        server: The FastMCP server instance
        config: Server configuration
    """
    # Register example tools
    register_tools(server)
    
    logger.info("Registered all tools with the server") 