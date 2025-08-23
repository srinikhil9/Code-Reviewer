#!/usr/bin/env python3
"""
Basic Usage Example for AI Code Review Assistant

This example demonstrates how to use the AI Code Review Assistant
programmatically through the Langflow API.
"""

import os
import json
import requests
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CodeReviewAssistant:
    """Client for interacting with the AI Code Review Assistant flow."""
    
    def __init__(
        self, 
        langflow_url: str = "http://localhost:7860",
        flow_id: Optional[str] = None
    ):
        """Initialize the Code Review Assistant client.
        
        Args:
            langflow_url: Base URL for Langflow API
            flow_id: ID of the deployed flow (optional)
        """
        self.langflow_url = langflow_url.rstrip('/')
        self.flow_id = flow_id
        self.session = requests.Session()
        
    def submit_task(
        self, 
        task: str, 
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Submit a coding task to the AI agents.
        
        Args:
            task: The coding task description
            session_id: Optional session ID for conversation tracking
            
        Returns:
            Dictionary containing the response from agents
            
        Example:
            >>> assistant = CodeReviewAssistant()
            >>> result = assistant.submit_task(
            ...     "Create a Python function to calculate prime numbers"
            ... )
            >>> print(result['generated_code'])
        """
        # Prepare the request payload
        payload = {
            "input_value": task,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                "ChatInput-o3j0G": {
                    "input_value": task,
                    "session_id": session_id or f"session_{int(time.time())}"
                }
            }
        }
        
        # Make API request
        url = f"{self.langflow_url}/api/v1/run/{self.flow_id or 'coding-reviewer'}"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_conversation_history(self, session_id: str) -> list:
        """Get conversation history for a session.
        
        Args:
            session_id: The session ID to retrieve history for
            
        Returns:
            List of conversation messages
        """
        url = f"{self.langflow_url}/api/v1/monitor/messages"
        params = {"session_id": session_id}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()


def main():
    """Main example function demonstrating various use cases."""
    
    # Initialize the assistant
    assistant = CodeReviewAssistant()
    
    # Example 1: Basic code generation
    print("🤖 Example 1: Basic Code Generation")
    print("-" * 50)
    
    task = "Create a Python function that validates email addresses using regex"
    result = assistant.submit_task(task)
    
    print(f"Task: {task}")
    print(f"Response: {result.get('outputs', [{}])[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('text', 'No response')}")
    print()
    
    # Example 2: Code review request
    print("🔍 Example 2: Code Review Request")
    print("-" * 50)
    
    code_to_review = '''
def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result = result * i
        return result
    '''
    
    review_task = f"Please review this code for improvements:\n\n```python\n{code_to_review}\n```"
    result = assistant.submit_task(review_task)
    
    print(f"Code to review:\n{code_to_review}")
    print(f"Review feedback: {result.get('outputs', [{}])[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('text', 'No response')}")
    print()
    
    # Example 3: Documentation request
    print("📝 Example 3: Documentation Request")  
    print("-" * 50)
    
    undocumented_code = '''
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
    '''
    
    doc_task = f"Add comprehensive documentation to this code:\n\n```python\n{undocumented_code}\n```"
    result = assistant.submit_task(doc_task)
    
    print(f"Original code:\n{undocumented_code}")
    print(f"Documented version: {result.get('outputs', [{}])[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('text', 'No response')}")
    print()
    
    # Example 4: Complex algorithm request
    print("⚡ Example 4: Complex Algorithm")
    print("-" * 50)
    
    algorithm_task = """
    Create a Python class that implements a LRU (Least Recently Used) cache 
    with the following requirements:
    - Fixed size capacity
    - O(1) get and put operations
    - Thread-safe implementation
    - Include comprehensive error handling
    """
    
    result = assistant.submit_task(algorithm_task)
    
    print(f"Algorithm request: {algorithm_task}")
    print(f"Generated solution: {result.get('outputs', [{}])[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('text', 'No response')}")
    print()


def batch_processing_example():
    """Example of processing multiple coding tasks in batch."""
    
    print("📦 Batch Processing Example")
    print("-" * 50)
    
    tasks = [
        "Create a function to reverse a string without using built-in methods",
        "Write a class for a simple stack data structure",
        "Implement a function to check if a string is a palindrome",
        "Create a decorator that measures function execution time",
        "Write a function that finds the longest common substring"
    ]
    
    assistant = CodeReviewAssistant()
    results = []
    
    for i, task in enumerate(tasks, 1):
        print(f"Processing task {i}/{len(tasks)}: {task[:50]}...")
        try:
            result = assistant.submit_task(task)
            results.append({
                'task': task,
                'success': True,
                'response': result.get('outputs', [{}])[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('text', 'No response')
            })
        except Exception as e:
            results.append({
                'task': task,
                'success': False,
                'error': str(e)
            })
        
        # Add small delay between requests
        time.sleep(1)
    
    # Print summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n✅ Batch processing complete: {successful}/{len(tasks)} tasks successful")
    
    return results


if __name__ == "__main__":
    try:
        print("🚀 AI Code Review Assistant - Basic Usage Examples")
        print("=" * 60)
        print()
        
        # Run main examples
        main()
        
        # Run batch processing example
        batch_results = batch_processing_example()
        
        # Save results to file
        with open('batch_results.json', 'w') as f:
            json.dump(batch_results, f, indent=2)
        print(f"📁 Results saved to batch_results.json")
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Langflow is running and the flow is properly imported.")