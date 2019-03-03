#!/bin/sh

source venv/bin/activate

python boot.py

exec gunicorn -b :5000 --access-logfile - --error-logfile - metadata_tool:app