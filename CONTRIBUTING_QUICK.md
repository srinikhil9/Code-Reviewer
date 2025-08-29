# Quick Contributing Guide

## 🚀 Getting Started Fast

1. **Clone and Setup**
   ```bash
   git clone https://github.com/srinikhil9/Code-Reviewer.git
   cd Code-Reviewer
   python scripts/quick_setup.py  # New! Quick environment check
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # For development:
   pip install -r requirements-dev.txt
   ```

3. **Test Your Setup**
   ```bash
   python cli.py status
   python cli.py generate "Create a simple function"
   ```

## 🔧 Development Workflow

```bash
# Format code
make format

# Run tests
make test

# Check everything
make check-all

# Quick validation
python scripts/validate_environment.py
```

## 💡 Quick Tips

- Use `python cli.py --help` for available commands
- Run `make help` to see all available make targets
- Check `python scripts/quick_setup.py` if you have issues
- See full guide in `CONTRIBUTING.md`

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Missing API key | `export OPENAI_API_KEY=your_key` |
| Import errors | `pip install -r requirements.txt` |
| Langflow not running | `langflow run` |
| Tests failing | `python scripts/validate_environment.py` |
