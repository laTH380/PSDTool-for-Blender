#!/bin/bash

uv pip freeze > requirements.txt
uv run pip install -r requirements.txt -t ex-library
# Compress-Archive -Path .\ex-library\* -DestinationPath .\ex-library.zip

# ./venv2exlib.sh