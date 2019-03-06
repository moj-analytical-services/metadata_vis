FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV FLASK_APP metadata_tool.py
COPY ./app /app

