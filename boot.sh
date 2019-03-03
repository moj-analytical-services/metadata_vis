#!/bin/sh

source venv/bin/activate

python boot.py

# exec gunicorn -b :8000 --access-logfile - --error-logfile - metadata_tool:app
python -m flask run --host=0.0.0.0 --port=80