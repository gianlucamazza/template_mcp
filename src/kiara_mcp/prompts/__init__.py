"""Prompts module for MCP server."""

from typing import Dict, List, Any
import logging
from ..config import ServerConfig

logger = logging.getLogger(__name__)


def get_prompts(config: ServerConfig) -> List[Dict[str, Any]]:
    """Get all prompt definitions for the server.
    
    Args:
        config: Server configuration
        
    Returns:
        List of prompt definitions
    """
    prompts = []
    
    # Add example prompt
    prompts.append({
        "name": "data-analysis",
        "description": "A prompt template for data analysis tasks",
        "template": """# Data Analysis Task

## Objective
Analyze the provided data to extract meaningful insights.

## Data Description
{data_description}

## Specific Questions
{questions}

## Analysis Approach
Please approach this analysis by:
1. Understanding the data structure
2. Cleaning and preprocessing if necessary
3. Applying appropriate analytical methods
4. Providing clear insights with visualizations when helpful
5. Summarizing key findings

## Additional Context
{additional_context}
""",
        "examples": [
            {
                "name": "Sales Data Analysis",
                "template_variables": {
                    "data_description": "Monthly sales data for the past year across all regions",
                    "questions": "What are the seasonal trends? Which region is performing best?",
                    "additional_context": "Company has recently expanded to the East region."
                }
            }
        ]
    })
    
    # Add more prompts here...
    
    logger.debug(f"Loaded {len(prompts)} prompts")
    return prompts 