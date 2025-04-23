"""Example tool implementation."""

import logging
from typing import Dict, Any, Optional

from mcp.server.fastmcp import Context

logger = logging.getLogger(__name__)


# Function to register tools with a server instance
def register_tools(server):
    """Register all tools with the server.
    
    Args:
        server: The FastMCP server instance
    """
    # Register tools using server's tool decorator
    @server.tool(name="echo", description="Echoes back the input message.")
    async def echo_message(message: str, ctx: Optional[Context] = None) -> str:
        """Echo the input message back to the user.
        
        Args:
            message: The message to echo
            ctx: The MCP context
            
        Returns:
            The echoed message
        """
        logger.info(f"Echo tool called with message: {message}")
        if ctx:
            await ctx.info(f"Processing message: {message}")
        
        # Just return the message
        return f"You said: {message}"
    
    @server.tool(name="count-chars", description="Counts characters in a message.")
    async def count_characters(message: str, ctx: Optional[Context] = None) -> Dict[str, Any]:
        """Count the characters in a message.
        
        Args:
            message: The message to analyze
            ctx: The MCP context
            
        Returns:
            A dictionary with character counts
        """
        logger.info(f"Count characters tool called with message: {message}")
        if ctx:
            await ctx.info(f"Analyzing message: {message}")
        
        # Count characters
        char_count = len(message)
        word_count = len(message.split())
        
        # Return the result
        return {
            "message": message,
            "character_count": char_count,
            "word_count": word_count,
            "uppercase_count": sum(1 for c in message if c.isupper()),
            "lowercase_count": sum(1 for c in message if c.islower()),
            "digit_count": sum(1 for c in message if c.isdigit()),
            "whitespace_count": sum(1 for c in message if c.isspace()),
        } 