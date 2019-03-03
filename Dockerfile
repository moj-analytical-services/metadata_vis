FROM python:3.6-alpine

RUN adduser -D metadata_tool

WORKDIR /home/metadata_tool

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app

COPY metadata_tool.py config.py boot.sh boot.py ./

RUN chmod +x boot.sh

ENV FLASK_APP metadata_tool.py

RUN chown -R metadata_tool:metadata_tool ./
USER metadata_tool

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]