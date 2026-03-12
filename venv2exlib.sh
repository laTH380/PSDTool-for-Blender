#!/bin/bash
set -euo pipefail

PY_TAG="${1:-$(python -c 'import sys; print(f"py{sys.version_info.major}{sys.version_info.minor}")')}"
TARGET_DIR="ex-library/${PY_TAG}"

uv pip freeze > requirements.txt
rm -rf "${TARGET_DIR}"
mkdir -p "${TARGET_DIR}"
uv pip install -r requirements.txt --target "${TARGET_DIR}"
# Compress-Archive -Path .\ex-library\* -DestinationPath .\ex-library.zip

# Linux/macOS:
# ./venv2exlib.sh
# Windows:
# powershell -ExecutionPolicy Bypass -File .\venv2exlib.ps1
