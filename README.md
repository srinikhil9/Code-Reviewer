# 🤖 AI Code Review Assistant

> Smart Multi-Agent System for Automated Code Generation, Review, and Documentation

A Langflow-based solution that orchestrates multiple AI agents to handle the complete code development lifecycle — from initial generation to review, documentation, and quality assurance.

## 🌟 Features

- **🧠 Intelligent Orchestration**: Smart routing between specialized agents
- **⚡ Code Generation**: Automated code writing based on requirements
- **🔍 Automated Review**: Comprehensive code analysis for errors and improvements
- **📝 Auto-Documentation**: Generates inline comments and docstrings
- **🔄 Feedback Loops**: Iterative improvement cycles
- **👤 Human-in-the-Loop**: Manual approval checkpoints
- **🛠️ Code Execution**: Built-in validation and testing

## 🏗️ Architecture

### Agent Workflow
```
User Input → Orchestrator → {
    ├── Code Generator (writes clean code)
    ├── Code Reviewer (finds issues & suggests fixes)
    ├── Documentation Agent (adds comments & docs)
    └── Fallback Agent (handles edge cases)
}
```

### Core Components
- **Conditional Router**: Routes tasks based on orchestrator decisions
- **Multi-Agent System**: Specialized agents for different tasks
- **Feedback Loop**: Sends code back for improvements if issues found
- **Code Execution Node**: Validates generated code
- **Human Approval**: Manual oversight and intervention points

## 🚀 Quick Start

> **New!** Use our CLI tool: `python cli.py --help` for easy interaction

### Prerequisites
- [Langflow](https://langflow.org/) installed
- OpenAI API key (or other LLM provider)
- Python 3.8+

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/srinikhil9/Code-Reviewer.git
   cd Code-Reviewer
   ```

2. Install Langflow (if not already installed)
   ```bash
   pip install langflow
   ```

3. Set up environment variables
   ```bash
   # optional, if you plan to run example scripts
   cp .env.example .env
   # Add your API keys to .env
   ```

4. Import the flow
   ```bash
   langflow run
   # Go to http://localhost:7860
   # Import the flows/Coding_Reviewer.json file (or your exported flow)
   ```

5. Validate installation
   ```bash
   # Test LangGraph runner
   python -m flows.run_langgraph "Create a simple hello world function"
   
   # Run tests (optional)
   pytest tests/
   
   # Check code formatting (optional)
   black --check .
   ruff check .
   ```

### Usage

1. Start Langflow
   ```bash
   langflow run
   ```

2. Load the Flow
   - Open Langflow UI
   - Import `flows/Coding_Reviewer.json`
   - Configure your API keys in the agent components

3. Run the System
   - Enter your coding task in the chat input
   - Watch as agents collaborate to generate, review, and document code
   - Approve or request changes at human checkpoints

### LangGraph Runner (alternative to Langflow UI)

Run the equivalent multi-agent flow with LangChain + LangGraph:

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables (or use a local .env)
   ```bash
   export OPENAI_API_KEY=your_key_here    # PowerShell: $env:OPENAI_API_KEY="..."
   export OPENAI_MODEL=gpt-4o            # optional
   ```

3. Run the flow
   ```bash
   python -m flows.run_langgraph "Create a Python function that validates email addresses using regex"
   ```

4. Optional: require manual approval during runs
   ```bash
   export ALLOW_HUMAN_INPUT=1
   python -m flows.run_langgraph "Implement an LRU cache in Python"
   ```

### Programmatic Example

See `example_usage.py` for a simple client using Langflow's API.

## 💡 Use Cases

Perfect for:
- **Code Generation**: Turn requirements into working code
- **Code Review Automation**: Systematic analysis of code quality
- **Documentation Generation**: Auto-generate comments and docs
- **Learning & Training**: Understand best practices through AI feedback
- **Quality Assurance**: Multi-stage validation before deployment

## 🔧 Customization

### Modify Agent Prompts
Each agent has customizable system prompts in the flow:
- Orchestrator, Code Generator, Code Reviewer, Documentation Agent

### Add New Agents
1. Create a new Agent component in Langflow
2. Connect to Conditional Router
3. Update routing logic in the router component
4. Configure agent-specific prompts and tools

### Configure Models
- Default: OpenAI GPT-4
- Supports: Anthropic Claude, Google models, local models via Ollama

## 🔧 Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```bash
# Ensure you're in the project directory and dependencies are installed
pip install -r requirements.txt
```

**2. API Key Errors**
```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your_key_here  # Linux/Mac
$env:OPENAI_API_KEY="your_key_here"  # Windows PowerShell
```

**3. Langflow Connection Issues**
```bash
# Ensure Langflow is running
langflow run --host 0.0.0.0 --port 7860
```

**4. Import Errors in Tests**
```bash
# Run tests from project root
pytest tests/ -v
```

## 📚 Documentation

- Extended README: `github_readme.md`
- LangGraph runner: `docs/LangGraph.md`
- Contributing Guide: `CONTRIBUTING.md`
- Suggested Repo Layout: `github_structure.md`
- Version History: `CHANGELOG.md`

## 🤝 Contributing

We welcome contributions! Please see our `CONTRIBUTING.md`.

## 📝 License

MIT — see `LICENSE`.
