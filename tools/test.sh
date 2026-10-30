#!/usr/bin/env bash
# Run the test suite in the repo's Python environment (.venv: python3 -m venv .venv; pip install torch from
# download.pytorch.org/whl/cpu, then -r requirements.txt).
cd "$(dirname "$0")/.." && exec .venv/bin/python -m pytest -q tests/ "$@"
