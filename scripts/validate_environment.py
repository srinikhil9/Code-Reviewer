#!/usr/bin/env python3
"""
Environment Validation Script for AI Code Review Assistant

This script validates that all required dependencies, environment variables,
and services are properly configured for the AI Code Review Assistant.
"""

import os
import sys
import subprocess
import importlib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None


@dataclass
class ValidationResult:
    """Result of a validation check."""
    name: str
    status: bool
    message: str
    suggestion: Optional[str] = None


class EnvironmentValidator:
    """Validates the environment for AI Code Review Assistant."""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.project_root = Path(__file__).parent.parent
    
    def validate_all(self) -> bool:
        """Run all validation checks."""
        checks = [
            self._check_python_version,
            self._check_core_dependencies,
            self._check_optional_dependencies,
            self._check_environment_variables,
            self._check_langflow_server,
            self._check_project_structure,
            self._check_api_connectivity,
            self._check_git_repository,
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.results.append(ValidationResult(
                    name=check.__name__.replace('_check_', '').replace('_', ' ').title(),
                    status=False,
                    message=f"Check failed: {e}",
                    suggestion="Please check the error and try again."
                ))
        
        return all(result.status for result in self.results)
    
    def _check_python_version(self):
        """Check if Python version is compatible."""
        min_version = (3, 8)
        current_version = sys.version_info[:2]
        
        if current_version >= min_version:
            self.results.append(ValidationResult(
                name="Python Version",
                status=True,
                message=f"Python {'.'.join(map(str, current_version))} is compatible"
            ))
        else:
            self.results.append(ValidationResult(
                name="Python Version",
                status=False,
                message=f"Python {'.'.join(map(str, current_version))} is too old",
                suggestion=f"Please upgrade to Python {'.'.join(map(str, min_version))} or higher"
            ))
    
    def _check_core_dependencies(self):
        """Check if core dependencies are installed."""
        core_deps = [
            "langchain",
            "langgraph", 
            "langchain_openai",
            "dotenv",
        ]
        
        missing = []
        for dep in core_deps:
            try:
                if dep == "dotenv":
                    importlib.import_module("dotenv")
                else:
                    importlib.import_module(dep)
            except ImportError:
                missing.append(dep)
        
        if not missing:
            self.results.append(ValidationResult(
                name="Core Dependencies",
                status=True,
                message="All core dependencies are installed"
            ))
        else:
            self.results.append(ValidationResult(
                name="Core Dependencies",
                status=False,
                message=f"Missing dependencies: {', '.join(missing)}",
                suggestion="Run: pip install -r requirements.txt"
            ))
    
    def _check_optional_dependencies(self):
        """Check if optional development dependencies are installed."""
        optional_deps = {
            "black": "Code formatting",
            "ruff": "Linting",
            "pytest": "Testing",
            "rich": "CLI output formatting",
            "click": "CLI framework"
        }
        
        missing = []
        for dep, purpose in optional_deps.items():
            try:
                importlib.import_module(dep)
            except ImportError:
                missing.append(f"{dep} ({purpose})")
        
        if not missing:
            self.results.append(ValidationResult(
                name="Optional Dependencies",
                status=True,
                message="All optional dependencies are available"
            ))
        else:
            self.results.append(ValidationResult(
                name="Optional Dependencies",
                status=False,
                message=f"Missing optional: {', '.join(missing)}",
                suggestion="Run: pip install -r requirements-dev.txt"
            ))
    
    def _check_environment_variables(self):
        """Check if required environment variables are set."""
        required_vars = ["OPENAI_API_KEY"]
        optional_vars = ["OPENAI_MODEL", "LANGFLOW_HOST", "LANGFLOW_PORT"]
        
        missing_required = [var for var in required_vars if not os.getenv(var)]
        missing_optional = [var for var in optional_vars if not os.getenv(var)]
        
        if not missing_required:
            message = "Required environment variables are set"
            if missing_optional:
                message += f" (Optional missing: {', '.join(missing_optional)})"
            
            self.results.append(ValidationResult(
                name="Environment Variables",
                status=True,
                message=message
            ))
        else:
            self.results.append(ValidationResult(
                name="Environment Variables",
                status=False,
                message=f"Missing required: {', '.join(missing_required)}",
                suggestion="Set environment variables or create a .env file"
            ))
    
    def _check_langflow_server(self):
        """Check if Langflow server is running."""
        if not HAS_REQUESTS:
            self.results.append(ValidationResult(
                name="Langflow Server",
                status=False,
                message="Cannot check Langflow (requests not installed)",
                suggestion="Install requests: pip install requests"
            ))
            return
        
        langflow_url = os.getenv("LANGFLOW_HOST", "localhost")
        langflow_port = os.getenv("LANGFLOW_PORT", "7860")
        url = f"http://{langflow_url}:{langflow_port}"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.results.append(ValidationResult(
                    name="Langflow Server",
                    status=True,
                    message=f"Langflow is running at {url}"
                ))
            else:
                self.results.append(ValidationResult(
                    name="Langflow Server",
                    status=False,
                    message=f"Langflow returned status {response.status_code}",
                    suggestion="Check Langflow configuration"
                ))
        except requests.exceptions.RequestException:
            self.results.append(ValidationResult(
                name="Langflow Server",
                status=False,
                message=f"Cannot connect to Langflow at {url}",
                suggestion="Start Langflow: langflow run"
            ))
    
    def _check_project_structure(self):
        """Check if project structure is correct."""
        required_files = [
            "flows/langgraph_flow.py",
            "flows/run_langgraph.py",
            "requirements.txt",
            "README.md",
        ]
        
        missing = []
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing.append(file_path)
        
        if not missing:
            self.results.append(ValidationResult(
                name="Project Structure",
                status=True,
                message="All required files are present"
            ))
        else:
            self.results.append(ValidationResult(
                name="Project Structure",
                status=False,
                message=f"Missing files: {', '.join(missing)}",
                suggestion="Ensure you're in the correct project directory"
            ))
    
    def _check_api_connectivity(self):
        """Check if we can connect to OpenAI API."""
        if not os.getenv("OPENAI_API_KEY"):
            self.results.append(ValidationResult(
                name="API Connectivity",
                status=False,
                message="Cannot test API without OPENAI_API_KEY",
                suggestion="Set OPENAI_API_KEY environment variable"
            ))
            return
        
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=5)
            # This will fail if the API key is invalid
            result = llm.invoke("test")
            
            self.results.append(ValidationResult(
                name="API Connectivity",
                status=True,
                message="OpenAI API is accessible"
            ))
        except Exception as e:
            self.results.append(ValidationResult(
                name="API Connectivity",
                status=False,
                message=f"API test failed: {str(e)[:100]}...",
                suggestion="Check your OPENAI_API_KEY and internet connection"
            ))
    
    def _check_git_repository(self):
        """Check if we're in a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                self.results.append(ValidationResult(
                    name="Git Repository",
                    status=True,
                    message="Project is in a git repository"
                ))
            else:
                self.results.append(ValidationResult(
                    name="Git Repository",
                    status=False,
                    message="Not in a git repository",
                    suggestion="Initialize git: git init"
                ))
        except FileNotFoundError:
            self.results.append(ValidationResult(
                name="Git Repository",
                status=False,
                message="Git is not installed",
                suggestion="Install git for version control"
            ))
    
    def print_results(self):
        """Print validation results."""
        if HAS_RICH and console:
            self._print_rich_results()
        else:
            self._print_plain_results()
    
    def _print_rich_results(self):
        """Print results using Rich formatting."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Check", style="dim", width=20)
        table.add_column("Status", width=10)
        table.add_column("Message", style="dim", width=40)
        table.add_column("Suggestion", style="italic", width=30)
        
        for result in self.results:
            status_icon = "✅" if result.status else "❌"
            status_text = "PASS" if result.status else "FAIL"
            suggestion = result.suggestion or ""
            
            table.add_row(
                result.name,
                f"{status_icon} {status_text}",
                result.message,
                suggestion
            )
        
        console.print("\n")
        console.print(Panel(table, title="[bold blue]Environment Validation Results[/bold blue]"))
        
        # Summary
        passed = sum(1 for r in self.results if r.status)
        total = len(self.results)
        
        if passed == total:
            console.print(f"\n[bold green]✅ All {total} checks passed! Environment is ready.[/bold green]")
        else:
            failed = total - passed
            console.print(f"\n[bold red]❌ {failed} of {total} checks failed. Please address the issues above.[/bold red]")
    
    def _print_plain_results(self):
        """Print results in plain text format."""
        print("\n" + "="*80)
        print("ENVIRONMENT VALIDATION RESULTS")
        print("="*80)
        
        for result in self.results:
            status = "PASS" if result.status else "FAIL"
            print(f"\n{result.name}: {status}")
            print(f"  Message: {result.message}")
            if result.suggestion:
                print(f"  Suggestion: {result.suggestion}")
        
        # Summary
        passed = sum(1 for r in self.results if r.status)
        total = len(self.results)
        
        print("\n" + "="*80)
        if passed == total:
            print(f"✅ All {total} checks passed! Environment is ready.")
        else:
            failed = total - passed
            print(f"❌ {failed} of {total} checks failed. Please address the issues above.")
        print("="*80)


def main():
    """Main entry point."""
    validator = EnvironmentValidator()
    all_passed = validator.validate_all()
    validator.print_results()
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
