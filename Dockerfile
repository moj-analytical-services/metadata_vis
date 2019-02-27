FROM python:3.6-alpine

RUN adduser -D metadata

WORKDIR /home/metadata

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app.db app.db

COPY app app

COPY test_docker.py test_docker.py

RUN python /home/metadata/test_docker.py
# COPY microblog.py config.py ./

# RUN chmod +x boot.sh

# ENV FLASK_APP microblog.py

# RUN chown -R microblog:microblog ./
# USER microblog

EXPOSE 5000
# ENTRYPOINT ["./boot.sh"]