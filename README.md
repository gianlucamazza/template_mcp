# Template MCP Server

A professional Model Context Protocol (MCP) server implementation that provides tools, resources, and prompts for LLM integration.

## Features

- Clean, modular architecture with separation of concerns
- Extensible design for adding custom tools, resources, and prompts
- Type-safe implementation with Pydantic
- Comprehensive documentation and examples
- Support for both stdio and SSE transport protocols
- Ready-to-use integration with Claude Desktop and other MCP-compatible LLMs
- Structured error handling following MCP specifications
- Robust input validation and sanitization
- Security-focused implementation with best practices

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

| Tool Name   | Description                    | Parameters                 | Error Handling                       |
| ----------- | ------------------------------ | -------------------------- | ------------------------------------ |
| echo        | Echoes back the input message  | `message`: Text to echo    | Validates message length and content |
| count-chars | Counts characters in a message | `message`: Text to analyze | Validates message length and content |

### Error Handling

All tools implement proper error handling according to MCP specifications:

- Input validation errors return structured responses with `isError: true`
- Detailed error messages help diagnose issues
- Robust error handling prevents crashes and resource leaks

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

# Run security checks
trunk check
```

### Code Quality

The project uses Trunk for code quality checks and includes configuration to:

- Run static analysis with Bandit, Ruff, and other tools
- Apply consistent code formatting with Black and isort
- Ignore appropriate warnings in test files
- Check for security vulnerabilities

### Adding Custom Tools

1. Create a new file in `src/template_mcp/tools/`
2. Implement your tool following the example in `example_tool.py`
3. Use the validation utilities in `input_validation.py` for parameter validation
4. Register your tool in `src/template_mcp/tools/__init__.py`

Example:

```python
# src/template_mcp/tools/math_tools.py
from typing import Dict, Any, Optional
from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field, ValidationError

from .input_validation import create_success_result, create_error_result

class SumParams(BaseModel):
    """Parameters for sum calculation."""
    numbers: list[float] = Field(..., description="List of numbers to sum")

async def calculate_sum(numbers: list[float], ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Calculate the sum of a list of numbers.

    Args:
        numbers: List of numbers to sum
        ctx: Optional MCP context

    Returns:
        Dictionary with the result following MCP format
    """
    try:
        # Validate parameters
        params = SumParams(numbers=numbers)

        if ctx:
            await ctx.info(f"Calculating sum of {len(params.numbers)} numbers")

        result = sum(params.numbers)

        # Return structured result
        return create_success_result([
            {
                "type": "json",
                "json": {
                    "input": params.numbers,
                    "sum": result,
                    "count": len(params.numbers),
                    "average": result / len(params.numbers) if params.numbers else 0
                }
            }
        ])
    except ValidationError as e:
        return create_error_result(f"Invalid input parameters - {str(e)}")
    except Exception as e:
        return create_error_result(str(e))

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

## Security Considerations

The server implements several security best practices:

- **Input Validation**: All parameters are validated using Pydantic models
- **Sanitization**: String inputs are checked for potentially harmful content
- **Path Traversal Protection**: Paths are validated to prevent directory traversal attacks
- **URL Validation**: URLs are checked against regex patterns and blocked domain lists
- **Error Handling**: Errors are handled properly without exposing sensitive information

## Connecting to MCP Hosts

This server can connect to any MCP-compatible host, such as:

- Claude Desktop
- ChatGPT with plugins
- Other LLM applications supporting the MCP standard

## Community and Resources

- [MCP GitHub Repository](https://github.com/anthropics/anthropic-cookbook/tree/main/model_context_protocol) - Official examples
- [FastMCP Documentation](https://github.com/FastMCP/fastmcp) - MCP implementation in Python
- [Claude Documentation](https://docs.anthropic.com/claude/docs) - Claude API documentation
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs/concepts/tools) - Official MCP spec

## License

MIT
