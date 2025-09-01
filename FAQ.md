# Frequently Asked Questions

## General Questions

**Q: What is AI Code Review Assistant?**  
A: It's a multi-agent system that helps generate, review, and document code using AI.

**Q: What programming languages are supported?**  
A: Currently focused on Python, with support for other languages planned.

**Q: Do I need an OpenAI API key?**  
A: Yes, you need an OpenAI API key to use the AI features.

## Setup Questions

**Q: How do I get started quickly?**  
A: Run `python scripts/quick_setup.py` to check your environment and get setup instructions.

**Q: Why am I getting import errors?**  
A: Make sure you've installed dependencies with `pip install -r requirements.txt`.

**Q: How do I use the CLI?**  
A: Try `python cli.py --help` to see all available commands.

## Usage Questions

**Q: Can I use this without Langflow?**  
A: Yes! Use the LangGraph runner: `python -m flows.run_langgraph "your task"`

**Q: How do I enable human approval?**  
A: Set `ALLOW_HUMAN_INPUT=1` in your environment variables.

**Q: Where can I find examples?**  
A: Check the `examples/` directory for usage examples.
