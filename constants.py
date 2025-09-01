"""Constants used throughout the AI Code Review Assistant."""

# Default models
DEFAULT_MODEL = "gpt-4o"
FALLBACK_MODEL = "gpt-3.5-turbo"

# Agent types
AGENT_TYPES = {
    "GENERATOR": "code_generator",
    "REVIEWER": "code_reviewer", 
    "DOCUMENTER": "documentation_agent",
    "FALLBACK": "fallback_agent"
}

# Response formats
OUTPUT_FORMATS = ["json", "text", "pretty"]

# File extensions
SUPPORTED_LANGUAGES = [".py", ".js", ".ts", ".java", ".cpp", ".c"]
