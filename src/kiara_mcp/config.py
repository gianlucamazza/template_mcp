"""Configuration module for MCP server."""

import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    """Server configuration."""
    
    server_name: str = Field(
        default="Template MCP Server",
        description="Name of the MCP server"
    )
    
    server_version: str = Field(
        default="0.1.0",
        description="Version of the server"
    )
    
    server_description: str = Field(
        default="A professional MCP server implementation",
        description="Description of the server"
    )
    
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    # Environment variables can be accessed directly here
    api_keys: Dict[str, Optional[str]] = Field(
        default_factory=lambda: {
            "example_api": os.getenv("EXAMPLE_API_KEY"),
            # Add more API keys as needed
        },
        description="API keys for external services"
    )
    
    # Configuration for resources
    resource_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration for resources"
    )
    
    # Configuration for tools
    tool_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration for tools"
    )
    
    # Configuration for prompts
    prompt_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration for prompts"
    )
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service.
        
        Args:
            service: Name of the service
            
        Returns:
            The API key if available, None otherwise
        """
        return self.api_keys.get(service) 