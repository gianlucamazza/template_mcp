"""Example tool implementation."""

import logging
from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field, ValidationError

from .input_validation import create_error_result, create_success_result

logger = logging.getLogger(__name__)


class EchoParams(BaseModel):
    """Parameters for echo message tool."""

    message: str = Field(..., description="The message to echo", min_length=1)


class CountCharsParams(BaseModel):
    """Parameters for count characters tool."""

    message: str = Field(..., description="The message to analyze", min_length=1)


# Function to register tools with a server instance
def register_tools(server):
    """Register all tools with the server.

    Args:
        server: The FastMCP server instance
    """

    # Register tools using server's tool decorator
    @server.tool(name="echo", description="Echoes back the input message.")
    async def echo_message(
        message: str, ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """Echo the input message back to the user.

        Args:
            message: The message to echo
            ctx: The MCP context

        Returns:
            Dictionary result with the echoed message or error
        """
        try:
            # Validate input parameters
            params = EchoParams(message=message)

            logger.info(f"Echo tool called with message: {params.message}")
            if ctx:
                await ctx.info(f"Processing message: {params.message}")

            # Return the result as a structured object using the helper function
            return create_success_result(
                [{"type": "text", "text": f"You said: {params.message}"}]
            )
        except ValidationError as e:
            logger.error(f"Parameter validation error: {e}")
            return create_error_result(f"Invalid input parameters - {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in echo tool: {e}", exc_info=True)
            return create_error_result(str(e))

    @server.tool(name="count-chars", description="Counts characters in a message.")
    async def count_characters(
        message: str, ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """Count the characters in a message.

        Args:
            message: The message to analyze
            ctx: The MCP context

        Returns:
            Dictionary result with character counts or error
        """
        try:
            # Validate input parameters
            params = CountCharsParams(message=message)

            logger.info(f"Count characters tool called with message: {params.message}")
            if ctx:
                await ctx.info(f"Analyzing message: {params.message}")

            # Count characters
            char_count = len(params.message)
            word_count = len(params.message.split())

            # Calculate other counts
            analysis_results = {
                "message": params.message,
                "character_count": char_count,
                "word_count": word_count,
                "uppercase_count": sum(1 for c in params.message if c.isupper()),
                "lowercase_count": sum(1 for c in params.message if c.islower()),
                "digit_count": sum(1 for c in params.message if c.isdigit()),
                "whitespace_count": sum(1 for c in params.message if c.isspace()),
            }

            # Return the result as a structured object using the helper function
            return create_success_result(
                [
                    {"type": "text", "text": "Analysis Results:"},
                    {"type": "json", "json": analysis_results},
                ]
            )
        except ValidationError as e:
            logger.error(f"Parameter validation error: {e}")
            return create_error_result(f"Invalid input parameters - {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in count-chars tool: {e}", exc_info=True)
            return create_error_result(str(e))
