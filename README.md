# Template MCP Server

A professional Model Context Protocol (MCP) server implementation that provides tools, resources, and prompts for LLM integration.

## Features

- Clean, modular architecture with separation of concerns
- Extensible design for adding custom tools, resources, and prompts
- Type-safe implementation with Pydantic
- Comprehensive documentation and examples
- Support for both stdio and SSE transport protocols
- Ready-to-use integration with Claude Desktop and other MCP-compatible LLMs

## Installation

```bash
# Clone the repository
git clone https://github.com/gianlucamazza/template-mcp.git
cd template-mcp

# Set up a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode
pip install -e ".[dev]"

# Install fastmcp dependency
pip install fastmcp
```

## Usage

### Running the Server

```bash
# Run the MCP server with stdio transport (default)
python run_server.py

# Run with debug mode enabled
python run_server.py --debug

# Run with SSE transport
python run_server.py --transport sse
```

### Integrating with Claude Desktop

To connect this server to Claude Desktop, add the following to your Claude Desktop configuration:

```json
"template-mcp": {
  "command": "/path/to/your/python",
  "args": [
    "/path/to/template-mcp/run_server.py",
    "--debug"
  ],
  "autoApprove": [
    "echo",
    "count-chars"
  ]
}
```

Be sure to use absolute paths for both the Python executable and the run_server.py script.

### Example Interaction

Once connected to Claude Desktop, you can use the provided tools:

```text
User: Count the characters in "Hello, Template MCP!"

Claude: I'll analyze this text using the count-chars tool.

Character count: 21
Word count: 3
Uppercase count: 3
Lowercase count: 14
Digit count: 0
Whitespace count: 2
```

## Configuration

Create a `.env` file in the root directory with your configuration:

```text
# API keys for external services
EXAMPLE_API_KEY=your_api_key_here

# Server configuration
DEBUG=false
```

## Available Tools

The Template MCP server comes with the following built-in tools:

| Tool Name   | Description                    | Parameters                 |
| ----------- | ------------------------------ | -------------------------- |
| echo        | Echoes back the input message  | `message`: Text to echo    |
| count-chars | Counts characters in a message | `message`: Text to analyze |

## Development

### Prerequisites

- Python 3.9 or higher
- pip

### Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Run type checking
mypy src/
```

### Adding Custom Tools

1. Create a new file in `src/template_mcp/tools/`
2. Implement your tool following the example in `example_tool.py`
3. Register your tool in `src/template_mcp/tools/__init__.py`

Example:

```python
# src/template_mcp/tools/math_tools.py
from typing import Dict, Any, Optional
from mcp.server.fastmcp import Context

async def calculate_sum(numbers: list[float], ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Calculate the sum of a list of numbers.

    Args:
        numbers: List of numbers to sum
        ctx: Optional MCP context

    Returns:
        Dictionary with the result
    """
    if ctx:
        await ctx.info(f"Calculating sum of {len(numbers)} numbers")

    result = sum(numbers)
    return {
        "input": numbers,
        "sum": result,
        "count": len(numbers),
        "average": result / len(numbers) if numbers else 0
    }

# In __init__.py
from .math_tools import calculate_sum

def setup_tools(server, config):
    # Register existing tools
    register_tools(server)

    # Register math tools
    server.tool(
        name="calculate-sum",
        description="Calculate the sum of a list of numbers"
    )(calculate_sum)
```

## Connecting to MCP Hosts

This server can connect to any MCP-compatible host, such as:

- Claude Desktop
- ChatGPT with plugins
- Other LLM applications supporting the MCP standard

## Community and Resources

- [MCP GitHub Repository](https://github.com/anthropics/anthropic-cookbook/tree/main/model_context_protocol) - Official examples
- [FastMCP Documentation](https://github.com/FastMCP/fastmcp) - MCP implementation in Python
- [Claude Documentation](https://docs.anthropic.com/claude/docs) - Claude API documentation

## License

MIT
