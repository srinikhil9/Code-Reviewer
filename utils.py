"""
Utility functions for AI Code Review Assistant

This module provides common utility functions used across the project.
"""

import re
import hashlib
from typing import List, Optional


def clean_code_output(code: str) -> str:
    """Clean and format code output from LLM responses.
    
    Args:
        code: Raw code string from LLM
        
    Returns:
        Cleaned code string
    """
    # Remove common markdown code block markers
    code = re.sub(r'^```(?:python|py)?\s*\n', '', code, flags=re.MULTILINE)
    code = re.sub(r'\n```\s*$', '', code, flags=re.MULTILINE)
    
    # Remove extra whitespace
    code = code.strip()
    
    return code


def extract_function_names(code: str) -> List[str]:
    """Extract function names from Python code.
    
    Args:
        code: Python code string
        
    Returns:
        List of function names found in the code
    """
    pattern = r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    matches = re.findall(pattern, code, re.MULTILINE)
    return matches


def generate_task_id(task: str) -> str:
    """Generate a unique ID for a task.
    
    Args:
        task: Task description string
        
    Returns:
        Short hash ID for the task
    """
    return hashlib.md5(task.encode()).hexdigest()[:8]


def validate_python_syntax(code: str) -> tuple[bool, Optional[str]]:
    """Validate Python code syntax.
    
    Args:
        code: Python code string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        compile(code, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e.msg} at line {e.lineno}"
    except Exception as e:
        return False, f"Error: {str(e)}"
