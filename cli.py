#!/usr/bin/env python3
"""
CLI wrapper for AI Code Review Assistant

This script provides a command-line interface for the AI Code Review Assistant,
making it easier to use without writing custom Python code.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from dotenv import load_dotenv

# Add the project root to the path so we can import flows
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from flows.langgraph_flow import run
from example_usage import CodeReviewAssistant

# Load environment variables
load_dotenv()

# Rich console for pretty output
console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AI Code Review Assistant CLI - Smart Multi-Agent Code Analysis"""
    pass


@cli.command()
@click.argument("task", required=True)
@click.option("--model", "-m", default=None, help="Override the default LLM model")
@click.option("--output", "-o", type=click.File('w'), help="Save output to file")
@click.option("--format", "output_format", type=click.Choice(['json', 'text', 'pretty']), 
              default='pretty', help="Output format")
@click.option("--interactive", "-i", is_flag=True, help="Enable human-in-the-loop mode")
def generate(task: str, model: Optional[str], output, output_format: str, interactive: bool):
    """Generate code using the LangGraph multi-agent flow."""
    
    console.print(Panel(f"[bold blue]Task:[/bold blue] {task}", title="Code Generation"))
    
    # Set environment for interactive mode
    if interactive:
        os.environ["ALLOW_HUMAN_INPUT"] = "1"
    
    try:
        # Run the LangGraph flow
        result = run(task)
        
        if output_format == "json":
            output_data = json.dumps(result, indent=2)
        elif output_format == "text":
            output_data = f"Decision: {result.get('decision', 'N/A')}\n"
            output_data += f"Generated Code:\n{result.get('generated_code', 'N/A')}\n"
            output_data += f"Review Feedback:\n{result.get('reviewer_feedback', 'N/A')}\n"
            output_data += f"Documented Code:\n{result.get('documented_code', 'N/A')}\n"
            output_data += f"Approval Status: {result.get('approval_status', 'N/A')}\n"
        else:  # pretty format
            _display_pretty_result(result)
            output_data = None
        
        # Save to file if requested
        if output and output_data:
            output.write(output_data)
            console.print(f"[green]✅ Output saved to {output.name}[/green]")
            
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("code_file", type=click.Path(exists=True))
@click.option("--langflow-url", default="http://localhost:7860", help="Langflow server URL")
@click.option("--flow-id", help="Specific flow ID to use")
def review(code_file: str, langflow_url: str, flow_id: Optional[str]):
    """Review code from a file using Langflow API."""
    
    console.print(Panel(f"[bold blue]Reviewing:[/bold blue] {code_file}", title="Code Review"))
    
    try:
        # Read the code file
        with open(code_file, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Create review task
        task = f"Please review this code for improvements:\n\n```python\n{code_content}\n```"
        
        # Use Langflow API
        assistant = CodeReviewAssistant(langflow_url=langflow_url, flow_id=flow_id)
        result = assistant.submit_task(task)
        
        # Display result
        response_text = assistant._extract_response_text(result)
        
        console.print(Panel(
            Syntax(code_content, "python", theme="monokai", line_numbers=True),
            title="Original Code"
        ))
        
        console.print(Panel(response_text, title="[bold green]Review Feedback[/bold green]"))
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("code_file", type=click.Path(exists=True))
@click.option("--output-file", "-o", help="Save documented code to file")
def document(code_file: str, output_file: Optional[str]):
    """Add documentation to code from a file."""
    
    console.print(Panel(f"[bold blue]Documenting:[/bold blue] {code_file}", title="Code Documentation"))
    
    try:
        # Read the code file
        with open(code_file, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Create documentation task
        task = f"Add comprehensive documentation to this code:\n\n```python\n{code_content}\n```"
        
        # Run the flow
        result = run(task)
        documented_code = result.get('documented_code', '')
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(documented_code)
            console.print(f"[green]✅ Documented code saved to {output_file}[/green]")
        else:
            console.print(Panel(
                Syntax(documented_code, "python", theme="monokai", line_numbers=True),
                title="[bold green]Documented Code[/bold green]"
            ))
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def status():
    """Check the status of required services and environment."""
    
    console.print(Panel("System Status Check", title="[bold blue]AI Code Review Assistant[/bold blue]"))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="dim", width=20)
    table.add_column("Status", width=15)
    table.add_column("Details", style="dim")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python", "✅ OK", f"Version {python_version}")
    
    # Check environment variables
    openai_key = "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Missing"
    table.add_row("OpenAI API Key", openai_key, "OPENAI_API_KEY")
    
    # Check dependencies
    try:
        import langchain
        import langgraph
        import langchain_openai
        table.add_row("Dependencies", "✅ OK", "Core packages installed")
    except ImportError as e:
        table.add_row("Dependencies", "❌ Missing", str(e))
    
    # Check Langflow connection
    try:
        import requests
        response = requests.get("http://localhost:7860", timeout=5)
        langflow_status = "✅ Running" if response.status_code == 200 else "❌ Error"
    except:
        langflow_status = "❌ Not running"
    
    table.add_row("Langflow Server", langflow_status, "http://localhost:7860")
    
    console.print(table)


def _display_pretty_result(result: dict):
    """Display the result in a pretty format using Rich."""
    
    # Display decision
    decision = result.get('decision', 'N/A')
    console.print(Panel(f"[bold yellow]Agent Decision:[/bold yellow] {decision}", title="Orchestrator"))
    
    # Display generated code
    generated_code = result.get('generated_code', '')
    if generated_code:
        console.print(Panel(
            Syntax(generated_code, "python", theme="monokai", line_numbers=True),
            title="[bold green]Generated Code[/bold green]"
        ))
    
    # Display review feedback
    feedback = result.get('reviewer_feedback', '')
    if feedback:
        console.print(Panel(feedback, title="[bold orange1]Review Feedback[/bold orange1]"))
    
    # Display documented code
    documented_code = result.get('documented_code', '')
    if documented_code and documented_code != generated_code:
        console.print(Panel(
            Syntax(documented_code, "python", theme="monokai", line_numbers=True),
            title="[bold blue]Documented Code[/bold blue]"
        ))
    
    # Display approval status
    approval = result.get('approval_status', 'N/A')
    approval_color = "green" if approval == "approved" else "red"
    console.print(Panel(f"[bold {approval_color}]Approval Status:[/bold {approval_color}] {approval}", title="Final Status"))


if __name__ == "__main__":
    cli()
