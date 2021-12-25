FROM python:3.9.9-slim

COPY requirements/common.txt requirements/common.txt
RUN pip install -U pip && pip install -r requirements/common.txt

COPY ./src /app/src
COPY ./bin /app/bin
COPY config.py /app/config.py
COPY wsgi.py /app/wsgi.py
WORKDIR /app

RUN useradd theater_api
USER theater_api

EXPOSE $PORT

ENTRYPOINT ["bash", "/app/bin/run.sh"]