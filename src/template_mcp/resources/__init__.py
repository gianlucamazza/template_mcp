"""Resources module for MCP server."""

import logging
from typing import Any, Dict, List

from ..config import ServerConfig
from .example_resource import example_resource_reader

logger = logging.getLogger(__name__)


def get_resources(config: ServerConfig) -> List[Dict[str, Any]]:
    """Get all resource definitions for the server.

    Args:
        config: Server configuration

    Returns:
        List of resource definitions
    """
    resources = []

    # Add example resource
    resources.append(
        {
            "name": "example-resource",
            "description": "An example resource that provides sample data",
            "reader": example_resource_reader,
        }
    )

    # Add more resources here...

    logger.debug(f"Loaded {len(resources)} resources")
    return resources
