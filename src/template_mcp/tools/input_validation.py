"""Input validation utilities for MCP tools."""

import logging
import re
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class ToolError(Exception):
    """Exception raised for tool errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize the exception.

        Args:
            message: Error message
            details: Additional error details
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


def create_error_result(
    error_message: str, details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a standardized error result object for MCP tools.

    Args:
        error_message: The error message
        details: Optional additional error details

    Returns:
        A properly formatted error result
    """
    error_content: List[Dict[str, Any]] = [
        {"type": "text", "text": f"Error: {error_message}"}
    ]

    # Add details if provided
    if details:
        error_content.append({"type": "json", "json": details})

    return {"isError": True, "content": error_content}


def create_success_result(
    content: List[Dict[str, Union[str, Dict[str, Any]]]],
) -> Dict[str, Any]:
    """Create a standardized success result object for MCP tools.

    Args:
        content: The content of the response

    Returns:
        A properly formatted success result
    """
    return {"content": content}


class StringParam(BaseModel):
    """Base model for string parameter validation."""

    value: str = Field(..., min_length=1)

    @field_validator("value")
    @classmethod
    def sanitize_string(cls, v: str) -> str:
        """Sanitize string input, removing potentially harmful characters.

        Args:
            v: The string value

        Returns:
            Sanitized string
        """
        # Basic sanitation for demonstration - adapt to your security needs
        if "<script" in v.lower():
            raise ValueError("Potential XSS attack detected")
        return v


class PathParam(StringParam):
    """Model for path parameter validation."""

    @field_validator("value")
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate path to prevent path traversal attacks.

        Args:
            v: The path value

        Returns:
            Validated path
        """
        # Check for path traversal attempts
        if ".." in v or "//" in v:
            raise ValueError("Path traversal attempt detected")

        # Check for absolute paths if not allowed
        if v.startswith("/") or v.startswith("\\"):
            raise ValueError("Absolute paths not allowed")

        return v


class URLParam(StringParam):
    """Model for URL parameter validation."""

    @field_validator("value")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL to ensure it's properly formatted and safe.

        Args:
            v: The URL value

        Returns:
            Validated URL
        """
        # Basic URL validation
        url_pattern = re.compile(
            r"^(?:http|https)://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ipv4
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not url_pattern.match(v):
            raise ValueError("Invalid URL format")

        # Block potentially dangerous URLs
        blocked_domains = ["evil.example.com"]
        for domain in blocked_domains:
            if domain in v:
                raise ValueError(f"Access to {domain} is blocked")

        return v
