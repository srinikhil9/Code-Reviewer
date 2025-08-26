import json
import os
import sys

from dotenv import load_dotenv
from flows.langgraph_flow import run


def main() -> None:
    load_dotenv()
    task = " ".join(sys.argv[1:]) or os.environ.get(
        "TASK", "Create a Python function that validates email addresses using regex"
    )
    result = run(task)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()


