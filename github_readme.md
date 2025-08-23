# 🤖 AI Code Review Assistant

> **Smart Multi-Agent System for Automated Code Generation, Review, and Documentation**

A sophisticated Langflow-based solution that orchestrates multiple AI agents to handle the complete code development lifecycle - from initial generation to review, documentation, and quality assurance.

![Flow Diagram](./assets/flow-diagram.png)

## 🌟 Features

- **🧠 Intelligent Orchestration** - Smart routing between specialized agents
- **⚡ Code Generation** - Automated code writing based on requirements
- **🔍 Automated Review** - Comprehensive code analysis for errors and improvements
- **📝 Auto-Documentation** - Generates inline comments and docstrings
- **🔄 Feedback Loops** - Iterative improvement cycles
- **👤 Human-in-the-Loop** - Manual approval checkpoints
- **🛠️ Code Execution** - Built-in validation and testing

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
- **Conditional Router** - Routes tasks based on orchestrator decisions
- **Multi-Agent System** - Specialized agents for different tasks
- **Feedback Loop** - Sends code back for improvements if issues found
- **Code Execution Node** - Validates generated code
- **Human Approval** - Manual oversight and intervention points

## 🚀 Quick Start

### Prerequisites
- [Langflow](https://langflow.org/) installed
- OpenAI API key (or other LLM provider)
- Python 3.8+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-code-review-assistant.git
   cd ai-code-review-assistant
   ```

2. **Install Langflow** (if not already installed)
   ```bash
   pip install langflow
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

4. **Import the flow**
   ```bash
   langflow run
   # Go to http://localhost:7860
   # Import the Coding_Reviewer.json file
   ```

### Usage

1. **Start Langflow**
   ```bash
   langflow run
   ```

2. **Load the Flow**
   - Open Langflow UI
   - Import `flows/Coding_Reviewer.json`
   - Configure your API keys in the agent components

3. **Run the System**
   - Enter your coding task in the chat input
   - Watch as agents collaborate to generate, review, and document code
   - Approve or request changes at human checkpoints

## 💡 Use Cases

### Perfect for:
- **Code Generation** - Turn requirements into working code
- **Code Review Automation** - Systematic analysis of code quality
- **Documentation Generation** - Auto-generate comments and docs
- **Learning & Training** - Understand best practices through AI feedback
- **Quality Assurance** - Multi-stage validation before deployment

### Example Tasks:
```
"Create a Python function to calculate fibonacci numbers"
"Write a REST API endpoint for user authentication"
"Build a React component for a todo list"
"Generate a SQL query to analyze sales data"
```

## 🛠️ Customization

### Modify Agent Prompts
Each agent has customizable system prompts in the flow:

- **Orchestrator**: Routes tasks to appropriate agents
- **Code Generator**: Focuses on clean, efficient code generation
- **Code Reviewer**: Analyzes for errors, security, and best practices  
- **Documentation Agent**: Adds comprehensive documentation

### Add New Agents
1. Create new Agent component in Langflow
2. Connect to Conditional Router
3. Update routing logic in router component
4. Configure agent-specific prompts and tools

### Configure Models
- Default: OpenAI GPT-4
- Supports: Anthropic Claude, Google PaLM, local models via Ollama
- Adjust in Agent → Model Provider settings

## 📊 Flow Components

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **Orchestrator Agent** | Task routing | Decides which specialized agent to use |
| **Conditional Router** | Flow control | Routes based on orchestrator decisions |
| **Code Generator** | Code creation | Writes clean, efficient code |
| **Code Reviewer** | Quality assurance | Finds errors, suggests improvements |
| **Documentation Agent** | Documentation | Adds comments, docstrings |
| **Feedback Loop** | Iteration control | Handles retry logic |
| **Code Execution** | Validation | Tests generated code |
| **Human-in-the-Loop** | Manual oversight | Approval checkpoints |

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here  # optional
LANGFLOW_HOST=localhost
LANGFLOW_PORT=7860
```

### Agent Settings
Each agent can be configured with:
- **Temperature**: Creativity vs consistency (0.1 = focused, 0.9 = creative)
- **Max Tokens**: Response length limits
- **Model**: Choose from available LLM providers
- **System Prompt**: Customize agent behavior

## 📈 Performance Tips

- **Use GPT-4** for best code quality (slower but more accurate)
- **Use GPT-3.5-turbo** for faster iterations (quicker but less sophisticated)
- **Adjust temperatures**: Lower for production code, higher for creative solutions
- **Enable human checkpoints** for critical applications

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup
```bash
git clone https://github.com/yourusername/ai-code-review-assistant.git
cd ai-code-review-assistant
pip install -r requirements.txt
pre-commit install
```

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Documentation**: [Wiki](../../wiki)
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Discord**: [Join our community](https://discord.gg/langflow)

## 🏆 Acknowledgments

- Built with [Langflow](https://langflow.org/)
- Powered by [OpenAI](https://openai.com/)
- Inspired by multi-agent AI research

---

⭐ **Star this repo if it helps you build better code!** ⭐