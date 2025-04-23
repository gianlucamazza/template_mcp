# template MCP Server

A professional Model Context Protocol (MCP) server implementation that provides tools, resources, and prompts for LLM integration.

## Features

- Clean, modular architecture
- Extensible design for adding new tools and resources
- Type-safe implementation with Pydantic
- Comprehensive documentation

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
```

## Usage

```bash
# Run the MCP server
template-mcp
```

## Configuration

Create a `.env` file in the root directory with your configuration:

```text
# API keys for external services
EXAMPLE_API_KEY=your_api_key_here
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
```

## Connecting to MCP Hosts

This server can connect to any MCP-compatible host, such as Claude Desktop or other LLM applications.

## License

MIT
