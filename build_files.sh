#!/bin/bash

# build_files.sh
echo "Building project..."
python3.12 -m pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput