## LangGraph Runner

### Install
```bash
pip install -r requirements.txt
```

### Configure
Create a `.env` at repo root or export env vars:
```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o  # optional
```

### Run
```bash
python -m flows.run_langgraph "Create a Python function that validates email addresses using regex"
```

### Human-in-the-loop (optional)
```bash
export ALLOW_HUMAN_INPUT=1
python -m flows.run_langgraph "Implement an LRU cache in Python"
```

### Output
The runner returns JSON with keys:
- `decision`: orchestrator route (GENERATE/REVIEW/DOCUMENT)
- `generated_code`: initial code
- `reviewer_feedback`: review summary
- `documented_code`: final documented code
- `approval_status`: approved/not approved

### Troubleshooting
- 401 invalid key: rotate key, verify `OPENAI_API_KEY` loaded
- Model not found: set `OPENAI_MODEL` to an available model
- Proxy/SSL issues: test with `python -c "from langchain_openai import ChatOpenAI; print(ChatOpenAI(model='gpt-4o').invoke('ping').content)"`

