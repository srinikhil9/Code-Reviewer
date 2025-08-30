"""
Configuration settings for AI Code Review Assistant

This module contains default configuration values and environment-based settings.
"""

import os
from typing import Dict, Any


# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "llm": {
        "model": "gpt-4o",
        "temperature": 0.1,
        "max_tokens": 2000,
    },
    "langflow": {
        "host": "localhost",
        "port": 7860,
        "timeout": 30,
    },
    "agents": {
        "max_retry_attempts": 3,
        "enable_human_approval": False,
    },
    "output": {
        "format": "pretty",
        "save_results": True,
        "output_dir": "output",
    }
}


def get_config() -> Dict[str, Any]:
    """Get configuration with environment variable overrides.
    
    Returns:
        Configuration dictionary with environment overrides applied
    """
    config = DEFAULT_CONFIG.copy()
    
    # LLM settings
    if os.getenv("OPENAI_MODEL"):
        config["llm"]["model"] = os.getenv("OPENAI_MODEL")
    
    # Langflow settings
    if os.getenv("LANGFLOW_HOST"):
        config["langflow"]["host"] = os.getenv("LANGFLOW_HOST")
    
    if os.getenv("LANGFLOW_PORT"):
        config["langflow"]["port"] = int(os.getenv("LANGFLOW_PORT"))
    
    # Agent settings
    if os.getenv("ALLOW_HUMAN_INPUT") == "1":
        config["agents"]["enable_human_approval"] = True
    
    return config


def get_api_key() -> str:
    """Get OpenAI API key from environment.
    
    Returns:
        API key string
        
    Raises:
        ValueError: If API key is not found
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key
