# 🤝 Contributing to AI Code Review Assistant

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## 🌟 Ways to Contribute

- **🐛 Bug Reports** - Help us identify and fix issues
- **💡 Feature Requests** - Suggest new capabilities
- **🔧 Code Contributions** - Submit improvements and new features
- **📖 Documentation** - Improve guides and examples
- **🧪 Testing** - Help test new features and edge cases
- **💬 Community Support** - Help others in discussions

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Langflow
- API keys for LLM providers

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-code-review-assistant.git
   cd ai-code-review-assistant
   ```

2. **Set up development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

## 📋 Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new features
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Test Langflow integration
   python scripts/run_flow.py --test
   
   # Manual testing
   langflow run
   # Import and test your modified flow
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new agent for code optimization"
   # Follow conventional commit format
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create Pull Request on GitHub
   ```

## 🎯 Coding Standards

### Python Code Style
- **PEP 8** compliance
- **Type hints** for function parameters and returns
- **Docstrings** for all public functions and classes
- **Meaningful variable names**

```python
def process_code_review(
    code_content: str, 
    review_criteria: Dict[str, Any]
) -> CodeReview:
    """Process code review using AI agents.
    
    Args:
        code_content: The source code to review
        review_criteria: Criteria for the review process
        
    Returns:
        CodeReview object with analysis results
        
    Raises:
        ValidationError: If code_content is invalid
    """
    # Implementation here
    pass
```

### Langflow Components
- **Clear component names** and descriptions
- **Proper input/output types**
- **Error handling** in custom components
- **Documentation** for complex logic

### Commit Message Format
Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add support for Claude-3 models
fix: resolve connection timeout in code execution
docs: update installation guide for Windows
refactor: simplify agent routing logic
test: add integration tests for feedback loop
```

## 🧪 Testing

### Test Types
- **Unit tests** - Test individual components
- **Integration tests** - Test component interactions
- **Flow tests** - Test complete Langflow workflows
- **Example tests** - Ensure examples work correctly

### Running Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/test_components.py

# With coverage
pytest --cov=utils --cov-report=html

# Integration tests (requires API keys)
pytest tests/test_integration.py --api-tests
```

### Writing Tests
```python
import pytest
from unittest.mock import Mock, patch

def test_code_generator_agent():
    """Test code generation with mock LLM."""
    with patch('openai.ChatCompletion.create') as mock_create:
        mock_create.return_value.choices = [
            Mock(message=Mock(content="def hello(): pass"))
        ]
        
        result = generate_code("Create a hello function")
        assert "def hello" in result
        assert callable(compile(result, '<string>', 'exec'))
```

## 📚 Documentation

### What to Document
- **New features** and components
- **Configuration options**
- **Usage examples**
- **Breaking changes**
- **Migration guides**

### Documentation Style
- **Clear and concise** language
- **Step-by-step** instructions
- **Code examples** with explanations
- **Screenshots** for UI changes
- **Links** to related documentation

## 🐛 Bug Reports

### Before Submitting
- **Search existing issues** to avoid duplicates
- **Test with latest version**
- **Reproduce the issue** consistently

### Bug Report Template
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Start Langflow
2. Import the flow
3. Run with input "..."
4. Observe error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 22.04
- Python: 3.9.7
- Langflow: 1.0.0
- LLM Provider: OpenAI GPT-4

## Additional Context
- Error messages
- Screenshots
- Flow configuration
```

## 💡 Feature Requests

### Feature Request Template
```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Implementation
How should this feature work?

## Alternatives Considered
Other approaches you've considered

## Additional Context
Mockups, examples, related issues
```

## 🔍 Code Review Process

### For Contributors
- **Self-review** your changes before submitting
- **Write clear PR descriptions**
- **Respond to feedback** promptly
- **Keep PRs focused** and reasonably sized

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No breaking changes without discussion
- [ ] Commit messages follow convention
- [ ] PR description explains changes clearly

## 🏆 Recognition

Contributors are recognized in:
- **README.md** contributors section
- **CHANGELOG.md** for significant contributions
- **GitHub releases** acknowledgments

## ❓ Questions?

- **GitHub Discussions** for general questions
- **Issues** for bugs and feature requests
- **Discord** for real-time chat
- **Email** for sensitive matters

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make AI Code Review Assistant better! 🚀