#!/usr/bin/env python3
"""
Quick Setup Script for AI Code Review Assistant

This script helps new users get started quickly by checking their environment
and providing step-by-step setup instructions.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print a welcome header."""
    print("🤖 AI Code Review Assistant - Quick Setup")
    print("=" * 50)

def check_python():
    """Check Python version."""
    version = sys.version_info
    if version >= (3, 8):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Too old")
        print("   Please upgrade to Python 3.8 or higher")
        return False

def check_git():
    """Check if git is installed."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git - Installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git - Not found")
        print("   Please install Git: https://git-scm.com/")
        return False

def check_api_key():
    """Check for OpenAI API key."""
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API Key - Set")
        return True
    else:
        print("❌ OpenAI API Key - Missing")
        print("   Set with: export OPENAI_API_KEY=your_key_here")
        return False

def main():
    """Main setup function."""
    print_header()
    
    checks = [
        ("Python Version", check_python),
        ("Git", check_git),
        ("API Key", check_api_key),
    ]
    
    results = []
    for name, check_func in checks:
        results.append(check_func())
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("🎉 All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Try the CLI: python cli.py status")
        print("3. Generate code: python cli.py generate 'Create a hello world function'")
    else:
        print("⚠️  Some issues need to be fixed before you can proceed.")
        print("Please address the items marked with ❌ above.")

if __name__ == "__main__":
    main()
