#!/usr/bin/env python3
"""Script to run the Template MCP server."""

import logging
import argparse
from template_mcp.server import create_server, run_server
from template_mcp.config import ServerConfig
from template_mcp.tools import setup_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Template MCP server")
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode"
    )
    parser.add_argument(
        "--transport", choices=["stdio", "sse"], default="stdio",
        help="Transport protocol to use (stdio or sse)"
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    # Parse arguments
    args = parse_args()
    
    # Create configuration
    config = ServerConfig(debug=args.debug)
    
    # Create server
    server = create_server(config)
    
    # Setup tools
    setup_tools(server, config)
    
    # Run the server
    logger.info(f"Starting Template MCP server with {args.transport} transport")
    run_server(server, transport=args.transport)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True) 