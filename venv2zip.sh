#!/bin/bash
rm -r ex-library
pip freeze > requirements.txt
pip3 install -r requirements.txt -t ex-library
# Compress-Archive -Path .\ex-library\* -DestinationPath .\ex-library.zip

# ./venv2zip.sh