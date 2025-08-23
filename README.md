# Code Reviewer

LangFlow-based code review pipeline. This repository hosts exported LangFlow flows and project metadata so you can version, collaborate, and deploy your flow.

## What is this?

This repo is a scaffold to publish your LangFlow project to GitHub. Store your flow exports under `flows/` and document how to use them.

## Quick start

1. Export your flow from LangFlow:
   - Open LangFlow and the flow you built
   - Click Export → JSON and download the file
   - Save it into `flows/` (for example: `flows/code-reviewer.json`)
2. Commit the exported JSON:
   - `git add flows/*.json`
   - `git commit -m "Add LangFlow export"`
   - `git push`

## Repository layout

- `flows/`: Place exported `.json` files from LangFlow here
- `.gitignore`: Common ignores for Python/Node/editor artifacts
- `LICENSE`: Project license (MIT)

## Using the flow

How you run the flow depends on your environment (LangFlow UI, SDK, or Docker). If you later add code or infra to run the flow programmatically, document it here.

## License

MIT — see `LICENSE`.


