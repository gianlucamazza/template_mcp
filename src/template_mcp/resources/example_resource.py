"""Example resource implementation."""

import logging
from typing import Dict, Any, Optional, AsyncGenerator, Tuple

logger = logging.getLogger(__name__)


async def example_resource_reader(
    path: Optional[str] = None
) -> AsyncGenerator[Tuple[Dict[str, Any], bytes], None]:
    """Example resource reader implementation.
    
    Args:
        path: Optional path parameter
        
    Yields:
        Tuples of (metadata, content) for each chunk of the resource
    """
    logger.info(f"Reading example resource with path: {path}")
    
    # Example metadata
    metadata = {
        "content_type": "text/plain",
        "total_size": 1024,  # Example size
        "created_at": "2023-08-01T12:00:00Z",
    }
    
    # Example content
    content = b"This is example content from a resource in the MCP server.\n"
    content += b"Resources can provide structured data to LLMs.\n"
    content += b"This could be data from files, databases, or APIs."
    
    # Yield the content
    yield metadata, content
    
    # In a real implementation, you might yield multiple chunks
    # for large resources or streaming data 