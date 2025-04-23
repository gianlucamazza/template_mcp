"""Tests for tools module."""

import pytest
from template_mcp.tools.example_tool import example_tool_function


@pytest.mark.asyncio
async def test_example_tool():
    """Test the example tool function."""
    # Prepare test input
    params = {
        "input_text": "Hello, world!",
        "option": "option2"
    }
    
    # Call the tool function
    result = await example_tool_function(params)
    
    # Verify the output
    assert "processed_text" in result
    assert "Processed: Hello, world!" == result["processed_text"]
    assert "option2" == result["selected_option"]
    assert 13 == result["character_count"] 