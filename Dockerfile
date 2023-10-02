FROM python:3.9-bullseye

RUN mkdir -p /opt/api/
RUN mkdir -p /var/log/api/
WORKDIR /opt/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ="Europe/Madrid"


RUN pip install --upgrade pip
COPY requirements.txt /opt/api/
RUN pip install -r requirements.txt

COPY app/. /opt/api/

ENTRYPOINT python /opt/api/api.py