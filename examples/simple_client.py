#!/usr/bin/env python3
"""Simple MCP client example for the Template MCP server."""

import asyncio
import sys
from contextlib import AsyncExitStack

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv()


class TemplateMCPClient:
    """Simple MCP client implementation for the Template MCP server."""

    def __init__(self):
        """Initialize the client."""
        self.session = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server.

        Args:
            server_script_path: Path to the server script
        """
        # Determine the command based on file extension
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )

        # Connect to the server
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        # Initialize the session
        await self.session.initialize()

        print("Connected to Template MCP server successfully")

    async def list_capabilities(self):
        """List all capabilities provided by the server."""
        if not self.session:
            print("Not connected to a server")
            return

        # List tools
        tools_response = await self.session.list_tools()
        print(f"\n=== Available Tools ({len(tools_response.tools)}) ===")
        for tool in tools_response.tools:
            print(f"  - {tool.name}: {tool.description}")

        # List resources
        resources_response = await self.session.list_resources()
        print(f"\n=== Available Resources ({len(resources_response.resources)}) ===")
        for resource in resources_response.resources:
            print(f"  - {resource.name}: {resource.description}")

        # List prompts
        prompts_response = await self.session.list_prompts()
        print(f"\n=== Available Prompts ({len(prompts_response.prompts)}) ===")
        for prompt in prompts_response.prompts:
            print(f"  - {prompt.name}: {prompt.description}")

    async def use_echo_tool(self, message: str):
        """Use the echo tool from the server.

        Args:
            message: Text message to echo
        """
        if not self.session:
            print("Not connected to a server")
            return

        print(f"\nCalling echo tool with message: '{message}'")

        # Prepare tool parameters
        params = {"message": message}

        # Call the tool
        response = await self.session.call_tool("echo", params)

        # Print the result
        print("\nTool response:")
        print(f"  {response}")

    async def use_count_chars_tool(self, message: str):
        """Use the count-chars tool from the server.

        Args:
            message: Text message to analyze
        """
        if not self.session:
            print("Not connected to a server")
            return

        print(f"\nCalling count-chars tool with message: '{message}'")

        # Prepare tool parameters
        params = {"message": message}

        # Call the tool
        response = await self.session.call_tool("count-chars", params)

        # Print the result
        print("\nTool response:")
        for field_name, field_value in response.__dict__.items():
            print(f"  {field_name}: {field_value}")

    async def close(self):
        """Close the connection to the server."""
        if self.exit_stack:
            await self.exit_stack.aclose()
            print("\nDisconnected from server")


async def main():
    """Main entry point.

    Example usage:
        python simple_client.py ../run_server.py
    """
    # Check command line arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path_to_server_script>")
        sys.exit(1)

    server_script_path = sys.argv[1]

    # Create client
    client = TemplateMCPClient()

    try:
        # Connect to server
        await client.connect_to_server(server_script_path)

        # List capabilities
        await client.list_capabilities()

        # Use echo tool
        await client.use_echo_tool("Hello from the Template MCP client!")

        # Use count-chars tool
        await client.use_count_chars_tool(
            "Testing the Template MCP server with a sample message. 123!"
        )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close connection
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
