#!/usr/bin/env python3
"""
Health Check Script for Production Deployments

This script provides a lightweight health check for the AI Code Review Assistant
when deployed in production environments like Docker containers.
"""

import sys
import os
import json
from pathlib import Path

def check_core_files():
    """Check if core application files exist."""
    required_files = [
        "flows/langgraph_flow.py",
        "flows/run_langgraph.py",
        "requirements.txt"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    return len(missing) == 0, missing

def check_environment():
    """Check critical environment variables."""
    required_vars = ["OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    return len(missing) == 0, missing

def check_imports():
    """Check if critical imports work."""
    try:
        import langchain
        import langgraph
        import langchain_openai
        return True, []
    except ImportError as e:
        return False, [str(e)]

def main():
    """Run health checks and return appropriate exit code."""
    checks = [
        ("Core Files", check_core_files),
        ("Environment", check_environment),
        ("Imports", check_imports),
    ]
    
    results = {}
    all_passed = True
    
    for name, check_func in checks:
        passed, issues = check_func()
        results[name] = {
            "passed": passed,
            "issues": issues
        }
        if not passed:
            all_passed = False
    
    # Output JSON for programmatic use
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
    else:
        # Human-readable output
        for name, result in results.items():
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"{name}: {status}")
            if result["issues"]:
                for issue in result["issues"]:
                    print(f"  - {issue}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
