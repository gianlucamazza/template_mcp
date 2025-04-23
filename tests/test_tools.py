"""Tests for tools module."""

import pytest

from template_mcp.tools.example_tool import register_tools


class MockServer:
    """Mock server class for testing."""

    def __init__(self):
        """Initialize the mock server."""
        self.tools = {}

    def tool(self, name, description):
        """Mock tool decorator."""

        def decorator(func):
            self.tools[name] = func
            return func

        return decorator


@pytest.mark.asyncio
async def test_echo_tool_success():
    """Test the echo tool function with valid input."""
    # Set up mock server and register tools
    mock_server = MockServer()
    register_tools(mock_server)

    # Call the echo tool with valid input
    result = await mock_server.tools["echo"]("Hello, world!")

    # Verify the output follows MCP structure
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    assert result["content"][0]["text"] == "You said: Hello, world!"
    assert "isError" not in result


@pytest.mark.asyncio
async def test_echo_tool_validation_error():
    """Test the echo tool function with empty input."""
    # Set up mock server and register tools
    mock_server = MockServer()
    register_tools(mock_server)

    # Call the echo tool with invalid input (empty string)
    result = await mock_server.tools["echo"]("")

    # Verify the output has proper error structure
    assert "isError" in result
    assert result["isError"] is True
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    assert "Error: Invalid input parameters" in result["content"][0]["text"]


@pytest.mark.asyncio
async def test_count_chars_tool_success():
    """Test the count characters tool with valid input."""
    # Set up mock server and register tools
    mock_server = MockServer()
    register_tools(mock_server)

    # Call the count-chars tool with valid input
    result = await mock_server.tools["count-chars"]("Hello, world!")

    # Verify the output follows MCP structure
    assert "content" in result
    assert len(result["content"]) == 2
    assert result["content"][0]["type"] == "text"
    assert result["content"][0]["text"] == "Analysis Results:"
    assert result["content"][1]["type"] == "json"

    # Verify JSON content
    json_content = result["content"][1]["json"]
    assert json_content["message"] == "Hello, world!"
    assert json_content["character_count"] == 13
    assert json_content["word_count"] == 2
    assert json_content["uppercase_count"] == 1
    assert json_content["lowercase_count"] == 9
    assert json_content["whitespace_count"] == 1
    assert "isError" not in result


@pytest.mark.asyncio
async def test_count_chars_tool_validation_error():
    """Test the count characters tool with empty input."""
    # Set up mock server and register tools
    mock_server = MockServer()
    register_tools(mock_server)

    # Call the count-chars tool with invalid input (empty string)
    result = await mock_server.tools["count-chars"]("")

    # Verify the output has proper error structure
    assert "isError" in result
    assert result["isError"] is True
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    assert "Error: Invalid input parameters" in result["content"][0]["text"]
