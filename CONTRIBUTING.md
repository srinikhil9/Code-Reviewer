# 🤝 Contributing to AI Code Review Assistant

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## 🌟 Ways to Contribute

- 🐛 Bug Reports
- 💡 Feature Requests
- 🔧 Code Contributions
- 📖 Documentation
- 🧪 Testing
- 💬 Community Support

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Langflow
- API keys for LLM providers

### Development Setup

1. Fork and clone the repository
```bash
git clone https://github.com/srinikhil9/Code-Reviewer.git
cd Code-Reviewer
```

2. (Optional) Set up a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies (if present)
```bash
pip install -r requirements.txt
```

4. Set up environment variables (if needed)
```bash
# Windows (PowerShell)
Copy-Item .env.example .env
# macOS/Linux
cp .env.example .env
# Add your API keys to .env
```

## 📋 Development Workflow

1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```
2. Make your changes (add tests/docs as needed)
3. Commit with conventional messages
```bash
git add .
git commit -m "feat: add amazing feature"
```
4. Push and open a Pull Request
```bash
git push origin feature/your-feature-name
```

## 🎯 Coding Standards

- PEP 8 for Python
- Type hints for public APIs
- Docstrings for functions and classes
- Clear component names and IO for Langflow custom components

## ✨ Code Style and Quality

To maintain a consistent and high-quality codebase, we use the following tools:

- **Black**: For automated code formatting.
- **Ruff**: For linting and identifying potential issues.

Please format your code before committing:
```bash
black .
ruff check . --fix
```

## 🧪 Testing

Add tests where applicable. If you include example scripts, ensure they run against a locally running Langflow instance.

## 🐛 Bug Reports / 💡 Feature Requests

Use GitHub Issues with clear reproduction steps or detailed proposals.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
